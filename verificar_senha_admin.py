#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect('ponto.db')
cursor = conn.cursor()

cursor.execute("SELECT id, nome, cpf, tipo, senha FROM usuarios WHERE tipo='admin'")
admin = cursor.fetchone()
conn.close()

if admin:
    print(f"Admin encontrado:")
    print(f"  ID: {admin[0]}")
    print(f"  Nome: {admin[1]}")
    print(f"  CPF: {admin[2]}")
    print(f"  Tipo: {admin[3]}")
    print(f"  Senha hash: {admin[4][:50]}...")
    print()
    
    # Testar senha
    senha_teste = 'Pont0!2024@Admin#Secure'
    resultado = check_password_hash(admin[4], senha_teste)
    print(f"Teste de senha '{senha_teste}':")
    print(f"  Resultado: {'✓ CORRETO' if resultado else '✗ INCORRETO'}")
else:
    print("Nenhum admin encontrado!")
