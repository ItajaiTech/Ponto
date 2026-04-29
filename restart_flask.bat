@echo off
REM Reinicia o servidor Flask matando processos antigos e iniciando um novo
cd /d %~dp0

REM Mata todos os processos python.exe que estejam rodando app.py
REM Limpa arquivo de sessão para derrubar todos os usuários logados
if exist session.db del /f /q session.db

REM Aguarda 2 segundos para garantir que os processos foram encerrados
timeout /T 2 >nul

REM Inicia o servidor Flask
start "RelogioPonto" cmd /c "cd /d %~dp0 && .venv\Scripts\python.exe app.py"
exit
