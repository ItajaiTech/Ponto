@echo off
REM Reinicia a aplicação abrindo uma janela de terminal visível
cd /d %~dp0
start "" cmd /k "cd /d %~dp0 && python app.py"
