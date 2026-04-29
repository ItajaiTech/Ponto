import re, json, sqlite3, calendar
from datetime import datetime, timedelta
from jinja2 import Template

# load DASHBOARD_HTML from app.py
with open('app.py','r',encoding='utf-8') as f:
    src = f.read()
m = re.search(r'DASHBOARD_HTML\s*=\s*"""(.*?)"""', src, re.S)
if not m:
    print('DASHBOARD_HTML not found')
    exit(1)
html_template = m.group(1)

# compute arrays for a sample user (same logic as dashboard)
conn = sqlite3.connect('ponto.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
user = c.execute("SELECT id,nome,tipo,jornada_diaria FROM usuarios WHERE tipo='funcionario' LIMIT 1").fetchone()
if not user:
    print('No funcionario found')
    exit(0)
uid = user['id']
nome = user['nome']
tipo = user['tipo']

# weekly
hoje = datetime.now()
inicio_semana = hoje - timedelta(days=hoje.weekday())
dias_semana = ['Seg','Ter','Qua','Qui','Sex']
horas_semana = []
for i in range(5):
    dia = (inicio_semana + timedelta(days=i)).date()
    registros = c.execute("SELECT data_hora FROM registros WHERE usuario_id=? AND date(data_hora)=?", (uid, dia)).fetchall()
    if len(registros) < 2:
        horas = 0
    else:
        registros_sorted = sorted([r['data_hora'] for r in registros])
        entrada = datetime.fromisoformat(registros_sorted[0])
        saida = datetime.fromisoformat(registros_sorted[-1])
        horas = round((saida - entrada).total_seconds()/3600,2)
    horas_semana.append(horas)

# monthly
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
    if len(registros) < 2:
        horas = 0
    else:
        registros_sorted = sorted([r['data_hora'] for r in registros])
        entrada = datetime.fromisoformat(registros_sorted[0])
        saida = datetime.fromisoformat(registros_sorted[-1])
        horas = round((saida - entrada).total_seconds()/3600,2)
    dias_mes.append(str(dia).zfill(2))
    horas_mes.append(horas)

conn.close()

# render template locally
tmpl = Template(html_template)
rendered = tmpl.render(
    nome=nome,
    tipo=tipo,
    dias=json.dumps(dias_semana),
    horas=json.dumps(horas_semana),
    dias_mes=json.dumps(dias_mes),
    horas_mes=json.dumps(horas_mes),
    jornada=user['jornada_diaria']
)

# save to file and print snippet
with open('dashboard_rendered_local.html','w',encoding='utf-8') as f:
    f.write(rendered)
print('Rendered to dashboard_rendered_local.html')
# show snippet where JS variables are
idx = rendered.find('let horasSemana=')
if idx!=-1:
    print('\n--- JS snippet ---\n')
    print(rendered[idx: idx+400])
else:
    print('JS variables not found in rendered template')
