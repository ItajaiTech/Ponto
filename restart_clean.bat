@echo off
REM restart_clean.bat
REM Pede elevação automática (Admin) e mata todos os processos Python nas portas 5000/5050
REM depois reinicia o Flask

setlocal enabledelayedexpansion

REM Verificar se está rodando como Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Elevando para Administrator...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb RunAs"
    exit /b
)

echo Limpando processos antigos nas portas 5000 e 5050...
cd /d %~dp0

REM Usar PowerShell para matar processos que escutam 5000 e 5050
powershell -Command "& {$pids = (Get-NetTCPConnection -State Listen -LocalPort 5000,5050 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique); foreach($id in $pids){ try { Stop-Process -Id $id -Force -ErrorAction Stop; Write-Output \"[KILLED] PID $id\" } catch { Write-Output \"[FAIL] PID $id - $_\" } }}"

timeout /T 2 >nul

REM Subir o Flask
echo.
echo Iniciando RelogioPonto...
echo.
start "RelogioPonto Flask" cmd /c "cd /d %~dp0 && .venv\Scripts\python.exe app.py"

echo Servidor iniciado! Acesse:
echo   - http://ponto.admin:5000 (porta principal)
echo   - http://ponto.admin:5050 (porta admin)
echo.
pause
