#!/usr/bin/env python3
"""
Script para testar o mecanismo de restart imediatamente
(sem aguardar 3 horas)
"""
import subprocess
import time
import os
from datetime import datetime

APP_DIR = r'C:\RelogioPonto'
LOG_FILE = os.path.join(APP_DIR, 'restart_scheduler.log')

def log_msg(msg):
    """Registra mensagem no log"""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception as e:
        print(f"Erro ao escrever log: {e}")

def kill_python_processes():
    """Mata todos os processos Python"""
    try:
        log_msg("  [1] Matando processos Python...")
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                'taskkill /F /IM python.exe /IM pythonw.exe',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode in (0, 128):  # 128 = processo não encontrado
                log_msg("  ✓ Processos Python interrompidos")
                return True
        return False
    except Exception as e:
        log_msg(f"  ✗ Erro ao matar processos: {e}")
        return False

def clean_session():
    """Limpa arquivo de sessão"""
    try:
        log_msg("  [2] Limpando session.db...")
        session_file = os.path.join(APP_DIR, 'session.db')
        if os.path.exists(session_file):
            os.remove(session_file)
            log_msg("  ✓ Session.db removido")
        else:
            log_msg("  ⓘ Session.db não existe (ok)")
        return True
    except Exception as e:
        log_msg(f"  ✗ Erro ao limpar session: {e}")
        return False

def start_app():
    """Inicia o app.py"""
    try:
        log_msg("  [3] Iniciando app.py...")
        os.chdir(APP_DIR)
        python_exe = os.path.join(APP_DIR, '.venv', 'Scripts', 'python.exe')
        app_py = os.path.join(APP_DIR, 'app.py')
        
        subprocess.Popen(
            [python_exe, app_py],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=APP_DIR
        )
        
        log_msg("  ✓ App.py iniciado em background")
        return True
    except Exception as e:
        log_msg(f"  ✗ Erro ao iniciar app.py: {e}")
        return False

def test_restart():
    """Executa restart para teste"""
    try:
        log_msg("="*60)
        log_msg(">>> TESTE DE RESTART AGORA <<<")
        log_msg("="*60)
        
        if not kill_python_processes():
            log_msg("AVISO: Falha ao matar processos")
        
        time.sleep(2)
        if not clean_session():
            log_msg("AVISO: Falha ao limpar session")
        
        time.sleep(1)
        if start_app():
            log_msg(">>> Restart completado com sucesso!")
            return True
        else:
            log_msg("ERRO: Falha ao iniciar app.py")
            return False
            
    except Exception as e:
        log_msg(f"ERRO: {e}")
        return False

if __name__ == '__main__':
    test_restart()
