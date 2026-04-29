import sqlite3

conn = sqlite3.connect('ponto.db')
c = conn.cursor()

# Inserir abono em 2026-02-05
c.execute("INSERT INTO registros (usuario_id, tipo, data_hora, justificativa) VALUES (2, 'abono', '2026-02-05 00:00:00', 'Teste abono')")
conn.commit()

# Verificar
count = c.execute("SELECT COUNT(*) FROM registros WHERE usuario_id=2 AND tipo='abono'").fetchone()[0]
print(f'Abonos totais para usuario 2: {count}')

# Ver feriados carregados
import json
try:
    with open('feriados_personalizados.json', 'r') as f:
        feriados = json.load(f)
        print(f'Feriados: {feriados}')
except:
    print('Arquivo de feriados inválido')

conn.close()
