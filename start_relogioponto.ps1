# Inicia o RelogioPonto usando o ambiente virtual proprio
$appPath = $PSScriptRoot
if (-not $appPath) {
    $appPath = Split-Path -Parent $MyInvocation.MyCommand.Path
}
$pythonExe = "$appPath\.venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "Nao encontrei $pythonExe" -ForegroundColor Red
    Write-Host "Crie o ambiente virtual do RelogioPonto antes de iniciar." -ForegroundColor Yellow
    exit 1
}

Set-Location $appPath
Write-Host "Iniciando RelogioPonto (portas 5000/5050 e redirects 6000/6050)" -ForegroundColor Green
& $pythonExe "$appPath\app.py"
