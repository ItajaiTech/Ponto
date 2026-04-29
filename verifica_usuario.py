import sqlite3
conn = sqlite3.connect('ponto.db')
cursor = conn.cursor()
cpf = '07562840903'
user = cursor.execute("SELECT * FROM usuarios WHERE replace(replace(cpf, '.', ''), '-', '')=?", (cpf,)).fetchone()
print(user)
conn.close()