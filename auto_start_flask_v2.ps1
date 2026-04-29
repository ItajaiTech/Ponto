# Script melhorado para iniciar o Flask automaticamente
# Este script deve ser registrado no Windows Task Scheduler para executar no startup
# Executar com: powershell -ExecutionPolicy Bypass -NoProfile -File auto_start_flask_v2.ps1

$appPath = $PSScriptRoot
if (-not $appPath) {
    $appPath = Split-Path -Parent $MyInvocation.MyCommand.Path
}
$pythonExe = "$appPath\.venv\Scripts\python.exe"
$appScript = "$appPath\app.py"
$logFile = "$appPath\auto_start.log"

# Função para registrar eventos
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -Append -FilePath $logFile -Encoding UTF8
}

Write-Log "Script iniciado"

# Aguarda 30 segundos para garantir que a rede subiu e o Windows terminou de carregar
Write-Log "Aguardando inicialização do Windows..."
Start-Sleep -Seconds 30

# Verifica se o Python da .venv existe (sem fallback)
if (-not (Test-Path $pythonExe)) {
    Write-Log "ERRO: Python da .venv não encontrado em $pythonExe"
    Write-Log "Abortando para evitar conflito com outro ambiente Python"
    exit 1
}

# Verifica se o app.py existe
if (-not (Test-Path $appScript)) {
    Write-Log "ERRO: app.py não encontrado em $appScript"
    exit 1
}

# Limpa sessão anterior para derrubar usuários logados
if (Test-Path "$appPath\session.db") {
    Remove-Item -Path "$appPath\session.db" -Force -ErrorAction SilentlyContinue
    Write-Log "Limpeza de sessão realizada"
}

# Inicia o Flask em background
Write-Log "Iniciando Flask..."
try {
    Set-Location $appPath
    $env:PONTO_HTTPS_PORT = "5000"
    $env:PONTO_HTTP_PORT = "6000"
    # Executa em background, sem janela visível
    $process = Start-Process -FilePath $pythonExe `
                            -ArgumentList $appScript `
                            -WindowStyle Hidden `
                            -PassThru `
                            -ErrorAction Stop
    if (-not $process -or -not $process.Id) {
        throw "Processo Python não retornou PID válido"
    }
    Write-Log "Flask iniciado com sucesso (PID: $($process.Id))"
} catch {
    Write-Log "ERRO ao iniciar Flask: $_"
    exit 1
}

Write-Log "Script concluído"
