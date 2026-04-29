#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para atualizar a senha do admin
"""
import sqlite3
from werkzeug.security import generate_password_hash

# Novas credenciais
cpf_admin = '00000000191'
nova_senha = 'Pont0!2024@Admin#Secure'
senha_hash = generate_password_hash(nova_senha)

try:
    conn = sqlite3.connect('ponto.db')
    cursor = conn.cursor()
    
    # Verificar se o admin existe
    cursor.execute("SELECT id, nome FROM usuarios WHERE cpf = ? AND tipo = 'admin'", (cpf_admin,))
    admin = cursor.fetchone()
    
    if admin:
        print(f"[✓] Admin encontrado: ID={admin[0]}, Nome={admin[1]}")
        
        # Atualizar a senha
        cursor.execute("UPDATE usuarios SET senha = ? WHERE cpf = ? AND tipo = 'admin'", (senha_hash, cpf_admin))
        conn.commit()
        
        print(f"[✓] Senha atualizada com sucesso!")
        print(f"\nNova credencial:")
        print(f"  CPF/Usuário: {cpf_admin}")
        print(f"  Senha: {nova_senha}")
        print(f"\nPara acessar o admin:")
        print(f"  URL: https://ponto.admin:5050 (ou https://127.0.0.1:5050)")
        print(f"  Insira as credenciais acima no formulário de login")
    else:
        print(f"[!] Admin com CPF {cpf_admin} não encontrado!")
        print("    Criando novo admin...")
        
        cursor.execute("""
            INSERT INTO usuarios (nome, cpf, senha, tipo, jornada_diaria)
            VALUES (?, ?, ?, 'admin', 8.0)
        """, ('Administrador', cpf_admin, senha_hash))
        conn.commit()
        
        print(f"[✓] Novo admin criado!")
        print(f"\nCredencial:")
        print(f"  CPF/Usuário: {cpf_admin}")
        print(f"  Senha: {nova_senha}")
    
    conn.close()

except Exception as e:
    print(f"[✗] Erro: {e}")
    import traceback
    traceback.print_exc()
