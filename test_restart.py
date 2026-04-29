#!/usr/bin/env python3
"""
Script de teste para validar o restart completo
"""
import restart_scheduler
import time

restart_scheduler.log_msg('===============================================')
restart_scheduler.log_msg('TESTE DE RESTART COMPLETO')
restart_scheduler.log_msg('===============================================')

# Executa restart
restart_scheduler.restart_flask()

restart_scheduler.log_msg('Aguardando app inicializar (5s)...')
time.sleep(5)

restart_scheduler.log_msg('Testando conexão HTTP...')
try:
    import urllib.request
    response = urllib.request.urlopen('http://127.0.0.1:5000', timeout=5)
    restart_scheduler.log_msg(f'✓ Servidor respondeu: HTTP {response.status}')
except Exception as e:
    restart_scheduler.log_msg(f'✗ Erro ao conectar: {e}')

restart_scheduler.log_msg('===============================================')
restart_scheduler.log_msg('TESTE FINALIZADO')
restart_scheduler.log_msg('===============================================')
