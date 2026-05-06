# Script para registrar autostart com privilégios elevados
$taskName = "RelogioPonto"
$scriptPath = "$PSScriptRoot\auto_start_flask_v2.ps1"

# Verificar se está rodando como admin
$isAdmin = ([Security.Principal.WindowsIdentity]::GetCurrent().Groups -match 'S-1-5-32-544').Count -gt 0

if (-not $isAdmin) {
    Write-Host "Reexecutando com privilégios de administrador..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "`n========================================="
Write-Host "Registrando Auto-Start do RelogioPonto"
Write-Host "=========================================`n"

# Remover tarefa anterior se existir
Write-Host "[1/3] Removendo tarefa anterior (se existir)..."
schtasks /delete /tn $taskName /f 2>&1 | Out-Null

# Criar nova tarefa
Write-Host "[2/3] Criando nova tarefa agendada..."
$command = "powershell -ExecutionPolicy Bypass -NoProfile -File `"$scriptPath`""
schtasks /create /tn $taskName `
    /tr $command `
    /sc onlogon `
    /ru $env:USERNAME `
    /f 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[3/3] Sucesso!`n"
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "TAREFA REGISTRADA COM SUCESSO!" -ForegroundColor Green
    Write-Host "=========================================`n" -ForegroundColor Green
    Write-Host "O programa RelogioPonto agora iniciará:"
    Write-Host "  - Automaticamente ao iniciar o Windows"
    Write-Host "  - Na sua conta de usuário ($env:USERNAME)"
    Write-Host "  - Depois de 30 segundos (para garantir rede pronta)`n"
    Write-Host "Logs de inicialização em: C:\RelogioPonto\auto_start.log"
    Write-Host "`nPara DESABILITAR o auto-start, execute:"
    Write-Host "  schtasks /delete /tn `"RelogioPonto`" /f"
} else {
    Write-Host "[3/3] ERRO ao criar a tarefa!" -ForegroundColor Red
    Write-Host "Código de erro: $LASTEXITCODE"
}

pause
