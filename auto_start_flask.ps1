# Script para iniciar o Flask automaticamente
# Executar com: powershell -ExecutionPolicy Bypass -File auto_start_flask.ps1

$appPath = "C:\RelogioPonto"
$pythonExe = "$appPath\.venv\Scripts\python.exe"
$appScript = "$appPath\app.py"

# Aguarda 30 segundos para garantir que a rede subiu (importante se usar IPs externos)
Start-Sleep -Seconds 30

# Limpa sessão anterior para derrubar usuários logados
if (Test-Path "$appPath\session.db") {
    Remove-Item -Path "$appPath\session.db" -Force -ErrorAction SilentlyContinue
}

# Inicia o Flask em background
Set-Location $appPath
& $pythonExe $appScript
