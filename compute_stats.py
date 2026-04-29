import sqlite3, calendar
from datetime import datetime, timedelta

def calcular_total_dia(registros):
    if len(registros) < 2:
        return 0
    registros.sort()
    entrada = datetime.fromisoformat(registros[0])
    saida = datetime.fromisoformat(registros[-1])
    total = (saida - entrada).total_seconds() / 3600
    return round(total, 2)

conn = sqlite3.connect('ponto.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
user = c.execute("SELECT id,nome,jornada_diaria FROM usuarios WHERE tipo='funcionario' LIMIT 1").fetchone()
if not user:
    print('No funcionario found')
    exit(0)
uid = user['id']
print('Using user:', uid, user['nome'])

# weekly (Mon-Fri)
hoje = datetime.now()
inicio_semana = hoje - timedelta(days=hoje.weekday())
horas_semana = []
dias_semana = ['Seg','Ter','Qua','Qui','Sex']
for i in range(5):
    dia = (inicio_semana + timedelta(days=i)).date()
    registros = c.execute("SELECT data_hora FROM registros WHERE usuario_id=? AND date(data_hora)=?", (uid, dia)).fetchall()
    horas = calcular_total_dia([r['data_hora'] for r in registros])
    horas_semana.append(horas)

# monthly (previous month)
primeiro_dia_mes_atual = datetime(hoje.year, hoje.month, 1)
ultimo_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
mes = ultimo_mes_anterior.month
ano = ultimo_mes_anterior.year
total_dias = calendar.monthrange(ano, mes)[1]
dias_mes = []
horas_mes = []
for dia in range(1, total_dias+1):
    data_base = datetime(ano, mes, dia).date()
    registros = c.execute("SELECT data_hora FROM registros WHERE usuario_id=? AND date(data_hora)=?", (uid, data_base)).fetchall()
    horas = calcular_total_dia([r['data_hora'] for r in registros])
    dias_mes.append(str(dia).zfill(2))
    horas_mes.append(horas)

print('\nHoras semana:', horas_semana)
print('Horas mes (first 10):', horas_mes[:10])
print('Total semana (sum):', sum(horas_semana))
print('Jornada diaria do usuario:', user['jornada_diaria'])
conn.close()
