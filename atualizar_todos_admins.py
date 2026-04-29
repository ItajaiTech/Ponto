#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from werkzeug.security import generate_password_hash

# Debug: Listar todos os admins
conn = sqlite3.connect('ponto.db')
cursor = conn.cursor()

print("Procurando admins no banco de dados...")
cursor.execute("SELECT id, nome, cpf, tipo FROM usuarios WHERE tipo='admin'")
admins = cursor.fetchall()

if admins:
    print(f"Encontrados {len(admins)} admin(s):")
    for admin in admins:
        print(f"  ID: {admin[0]}, Nome: {admin[1]}, CPF: {admin[2]}")
    print()
    
    # Atualizar todos os admins
    nova_senha = 'Pont0!2024@Admin#Secure'
    senha_hash = generate_password_hash(nova_senha)
    
    cursor.execute("UPDATE usuarios SET senha = ? WHERE tipo = 'admin'", (senha_hash,))
    conn.commit()
    
    linhas_afetadas = cursor.rowcount
    print(f"[✓] Senha atualizada para {linhas_afetadas} admin(s)")
    print(f"    Nova senha: {nova_senha}")
    print()
    print("Credenciais dos admins:")
    
    cursor.execute("SELECT id, nome, cpf FROM usuarios WHERE tipo='admin'")
    for admin in cursor.fetchall():
        print(f"  CPF: {admin[2]} | Nome: {admin[1]}")
else:
    print("[!] Nenhum admin encontrado!")
    print("    Criando novo admin com CPF 00000000000...")
    
    nova_senha = 'Pont0!2024@Admin#Secure'
    senha_hash = generate_password_hash(nova_senha)
    
    cursor.execute("""
        INSERT INTO usuarios (nome, cpf, senha, tipo, jornada_diaria)
        VALUES (?, ?, ?, 'admin', 8.0)
    """, ('Administrador', '00000000000', senha_hash))
    conn.commit()
    
    print(f"[✓] Admin criado!")
    print(f"    CPF: 00000000000")
    print(f"    Senha: {nova_senha}")

conn.close()
