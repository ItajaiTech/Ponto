@echo off
REM Script para registrar o startup automatico no Windows Task Scheduler
REM Execute este arquivo como ADMINISTRADOR
REM Clique com botão direito -> "Executar como administrador"

setlocal enabledelayedexpansion

echo.
echo =========================================
echo Registrando Auto-Start do RelogioPonto
echo =========================================
echo.

REM Verifica se esta rodando como admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERRO: Este script deve ser executado como ADMINISTRADOR!
    echo.
    echo Clique com botão direito do mouse neste arquivo e selecione:
    echo "Executar como administrador"
    pause
    exit /b 1
)

echo [1/3] Removendo tarefa anterior (se existir)...
schtasks /delete /tn "RelogioPonto" /f >nul 2>&1

echo [2/3] Criando nova tarefa agendada...
schtasks /create /tn "RelogioPonto" ^
    /tr "powershell -ExecutionPolicy Bypass -NoProfile -File C:\RelogioPonto\Ponto\auto_start_flask_v2.ps1" ^
    /sc onlogon ^
    /ru %USERNAME% ^
    /f

if %errorLevel% neq 0 goto fail

echo [3/3] Sucesso!
echo.
echo =========================================
echo TAREFA REGISTRADA COM SUCESSO!
echo =========================================
echo.
echo O programa RelogioPonto agora iniciara:
echo - Automaticamente ao iniciar o Windows
echo - Na sua conta de usuario: %USERNAME%
echo - Depois de 30 segundos para garantir que a rede esta pronta
echo.
echo Logs de inicializacao estarao em:
echo C:\RelogioPonto\Ponto\auto_start.log
echo.
echo Para DESABILITAR o auto-start, use:
echo   schtasks /delete /tn "RelogioPonto" /f
echo.
goto end

:fail
echo ERRO ao criar a tarefa!
echo Por favor, verifique se voce executou como ADMINISTRADOR.

:end

pause
