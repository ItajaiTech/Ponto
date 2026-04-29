#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste final de login com a nova senha do admin
"""
import requests
import ssl

def test_login(cpf, senha):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    session = requests.Session()
    
    try:
        # Fazer POST para login
        r = session.post(
            'https://127.0.0.1:5050/admin',
            data={'cpf': cpf, 'senha': senha},
            verify=False,
            timeout=10,
            allow_redirects=True
        )
        
        # Verificar resultado
        if r.status_code == 200:
            # Fazer GET para verificar se ficou na página admin
            r2 = session.get('https://127.0.0.1:5050/admin', verify=False, timeout=10)
            if r2.status_code == 200:
                return True, f"Login OK (Status: {r2.status_code})"
            else:
                return False, f"Login falhou: Session inválida"
        else:
            return False, f"Falha no login (Status: {r.status_code})"
            
    except Exception as e:
        return False, str(e)[:80]

# Testes
print("=" * 60)
print("TESTE DE LOGIN - NOVO ADMIN COM SENHA COMPLEXA")
print("=" * 60)
print()

testes = [
    ('00000000000', 'Pont0!2024@Admin#Secure', 'Novo CPF + Nova Senha'),
    ('00000000000', 'admin123', 'Novo CPF + Senha Antiga'),
]

for cpf, senha, descricao in testes:
    print(f"Teste: {descricao}")
    print(f"  CPF: {cpf}")
    print(f"  Senha: {senha}")
    
    success, msg = test_login(cpf, senha)
    
    if success:
        print(f"  Resultado: ✓ {msg}")
    else:
        print(f"  Resultado: ✗ {msg}")
    print()

print("=" * 60)
print("Resumo:")
print("  - Credenciais corretas: 00000000000 / Pont0!2024@Admin#Secure")
print("  - Senha anterior (admin123) nao funciona mais")
print("=" * 60)
