import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('ponto.db')
cursor = conn.cursor()

cpf = '00000000191'  # CPF fictício válido para testes
nome = 'Administrador'
senha = 'Pont0!2024@Admin#Secure'  # senha complexa: maiúsculas, minúsculas, números, caracteres especiais
senha_hash = generate_password_hash(senha)
tipo = 'admin'
jornada = 8.0

cursor.execute("""
    INSERT OR IGNORE INTO usuarios (nome, cpf, senha, tipo, jornada_diaria)
    VALUES (?, ?, ?, ?, ?)
""", (nome, cpf, senha_hash, tipo, jornada))

conn.commit()
print('Usuário admin criado com sucesso!')
conn.close()