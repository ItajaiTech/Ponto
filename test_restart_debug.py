#!/usr/bin/env python3
"""
Teste super simples de restart com debug detalhado
"""
import subprocess
import time
import os

APP_DIR = r'C:\RelogioPonto'

print("\n" + "="*70)
print(">>> TESTE DE RESTART - VERSÃO DEBUG <<<")
print("="*70)

# ETAPA 1: MATAR
print("\n[1] Matando processos Python...")
try:
    result = subprocess.run(
        'taskkill /F /IM python.exe',
        shell=True,
        capture_output=True,
        timeout=10
    )
    print(f"    Retorno: {result.returncode}")
    print("    ✓ Processos mortos")
except Exception as e:
    print(f"    ✗ Erro: {e}")

time.sleep(2)

# ETAPA 2: VERIFICAR MORTOS
print("\n[2] Verificando processos...")
try:
    result = subprocess.run(
        'tasklist | find /i "python"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.stdout.strip():
        print(f"    Encontrado: {result.stdout.strip()}")
    else:
        print("    ✓ Nenhum processo Python ativo")
except Exception as e:
    print(f"    Erro ao listar: {e}")

time.sleep(1)

# ETAPA 3: INICIAR
print("\n[3] Iniciando app.py...")
try:
    os.chdir(APP_DIR)
    python_exe = os.path.join(APP_DIR, '.venv', 'Scripts', 'python.exe')
    app_py = os.path.join(APP_DIR, 'app.py')
    
    # Usar START command do CMD
    cmd = f'START "" "{python_exe}" "{app_py}"'
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        timeout=5
    )
    print(f"    Retorno: {result.returncode}")
    print("    ✓ START command executado")
except Exception as e:
    print(f"    ✗ Erro: {e}")

time.sleep(3)

# ETAPA 4: VERIFICAR RODANDO
print("\n[4] Verificando se Flask reiniciou...")
try:
    result = subprocess.run(
        'tasklist | find /i "python"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.stdout.strip():
        print(f"    ✓ Encontrado: {result.stdout.strip()}")
        print("\n" + "="*70)
        print("✓✓✓ RESTART FUNCIONOU COM SUCESSO ✓✓✓")
        print("="*70 + "\n")
    else:
        print("    ✗ Nenhum processo Python detectado!")
        print("\n" + "="*70)
        print("✗✗✗ RESTART FALHOU - Flask não reiniciou ✗✗✗")
        print("="*70 + "\n")
except Exception as e:
    print(f"    Erro: {e}")
