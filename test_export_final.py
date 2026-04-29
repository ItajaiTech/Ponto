#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste final do export com todas as mudanças aplicadas
"""
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

print("Iniciando teste final...")

# Criar sessão com retry
session = requests_retry_session()

# Fazer login
print("1. Fazendo login...")
login_data = {
    'cpf': '00000000000',
    'senha': 'Pont0!2024@Admin#Secure'
}

try:
    r = session.post('http://localhost:5050/admin', data=login_data, timeout=10)
    print(f"   Status: {r.status_code}")
    
    # Aguardar processamento
    time.sleep(1)
    
    # Exportar Excel
    print("2. Exportando Excel...")
    export_url = 'http://localhost:5050/admin/espelho/export?tipo=excel&mes=2&ano=2026'
    r = session.get(export_url, timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Tamanho: {len(r.content)} bytes")
    
    # Verificar se é Zip válido (Excel)
    if r.content[:2] == b'PK':
        print("   ✅ Arquivo é um ZIP válido (Excel)")
        
        # Salvar
        with open('espelho_export_final.xlsx', 'wb') as f:
            f.write(r.content)
        print("   ✅ Arquivo salvo como: espelho_export_final.xlsx")
    else:
        print(f"   ❌ Erro: não é um arquivo válido")
        print(f"   Primeiros bytes: {r.content[:100]}")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n✅ Teste concluído!")
