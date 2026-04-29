#!/usr/bin/env python3
"""
Script para testar o mecanismo de restart com melhor tratamento de background
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
        if os.name == 'nt':
            result = subprocess.run(
                'taskkill /F /IM python.exe /IM pythonw.exe',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode in (0, 128):
                log_msg("  ✓ Processos Python interrompidos com sucesso")
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
            log_msg("  ⓘ Session.db não existe")
        return True
    except Exception as e:
        log_msg(f"  ✗ Erro ao limpar session: {e}")
        return False

def start_app_via_powershell():
    """Inicia app.py via PowerShell Start-Process (melhor para background)"""
    try:
        log_msg("  [3] Iniciando app.py em background...")
        os.chdir(APP_DIR)
        python_exe = os.path.join(APP_DIR, '.venv', 'Scripts', 'python.exe')
        app_py = os.path.join(APP_DIR, 'app.py')
        
        # Usar PowerShell Start-Process para melhor controle de background
        ps_cmd = f"""
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = '{python_exe}'
        $psi.Arguments = '{app_py}'
        $psi.WorkingDirectory = '{APP_DIR}'
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true
        [System.Diagnostics.Process]::Start($psi) | Out-Null
        """
        
        subprocess.run(
            ['powershell', '-Command', ps_cmd],
            capture_output=True,
            timeout=5
        )
        
        log_msg("  ✓ App.py iniciado com sucesso")
        return True
    except Exception as e:
        log_msg(f"  ✗ Erro ao iniciar app.py: {e}")
        return False

def test_restart():
    """Executa restart para teste"""
    try:
        log_msg("="*70)
        log_msg(">>> TESTE COMPLETO DE RESTART COM RECUPERAÇÃO <<<")
        log_msg("="*70)
        
        # Etapa 1: Matar
        if not kill_python_processes():
            log_msg("⚠ Falha ao matar processos, continuando...")
        
        time.sleep(2)
        
        # Etapa 2: Limpar
        if not clean_session():
            log_msg("⚠ Falha ao limpar session, continuando...")
        
        time.sleep(1)
        
        # Etapa 3: Reiniciar
        if start_app_via_powershell():
            log_msg("="*70)
            log_msg("✓✓✓ RESTART COMPLETADO COM SUCESSO ✓✓✓")
            log_msg("="*70)
            return True
        else:
            log_msg("✗✗✗ ERRO: Falha ao reiniciar app.py ✗✗✗")
            return False
            
    except Exception as e:
        log_msg(f"ERRO GERAL: {e}")
        return False

if __name__ == '__main__':
    test_restart()
