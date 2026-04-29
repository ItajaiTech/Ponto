import sqlite3
conn = sqlite3.connect('ponto.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(registros)")
schema = cursor.fetchall()
for col in schema:
    print(f"{col[1]}: {col[2]}")
