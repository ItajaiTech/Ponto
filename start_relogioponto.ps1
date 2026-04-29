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
$env:PONTO_HTTPS_PORT = "5000"
$env:PONTO_HTTP_PORT = "6000"
Write-Host "Iniciando RelogioPonto (backend HTTPS 5000 e HTTP 6000 para proxy)" -ForegroundColor Green
& $pythonExe "$appPath\app.py"
