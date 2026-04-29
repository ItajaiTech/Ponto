#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste simples e direto de export
"""
import requests
import sys

session = requests.Session()

print("1. Login...")
r = session.post('http://localhost:5050/', data={'cpf': '00000000000', 'senha': 'Pont0!2024@Admin#Secure'}, allow_redirects=True)
print(f"   OK - URL: {r.url}")

print("2. Admin...")
r = session.get('http://localhost:5050/admin')
print(f"   OK - Status: {r.status_code}")

print("3. Export...")
sys.stdout.flush()
try:
    r = session.get('http://localhost:5050/admin/espelho/export?tipo=excel&mes=02&ano=2026', timeout=15)
    print(f"   Status: {r.status_code}")
    print(f"   Tamanho: {len(r.content)}")
    
    if r.content[:2] == b'PK':
        print("   ✅ É Excel!")
        with open('espelho_admin_final.xlsx', 'wb') as f:
            f.write(r.content)
        print("   Salvo em: espelho_admin_final.xlsx")
    else:
        print(f"   ❌ Não é Excel. Primeiros bytes: {r.content[:50]}")
except Exception as e:
    print(f"   ❌ Erro: {e}")
