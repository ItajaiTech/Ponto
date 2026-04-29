import sqlite3, json, urllib.request, sys
from datetime import datetime, timedelta

url = 'http://localhost:5000/dashboard'
print('Fetching', url)
try:
    r = urllib.request.urlopen(url, timeout=10)
    html = r.read().decode('utf-8')
    print('\n--- HTML SNIPPET (first 2000 chars) ---')
    print(html[:2000])
except Exception as e:
    print('Error fetching dashboard:', e)
    html = ''

print('\n--- DB inspection ---')
try:
    conn = sqlite3.connect('ponto.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    total = c.execute('SELECT COUNT(*) as cnt FROM registros').fetchone()['cnt']
    print('Total registros:', total)
    users = c.execute('SELECT id,nome FROM usuarios').fetchall()
    print('Usuarios found:', len(users))
    for u in users:
        uid = u['id']
        name = u['nome']
        last30 = (datetime.now() - timedelta(days=30)).date()
        count30 = c.execute("SELECT COUNT(*) as cnt FROM registros WHERE usuario_id=? AND date(data_hora)>=?", (uid, last30)).fetchone()['cnt']
        last5 = c.execute("SELECT data_hora,tipo FROM registros WHERE usuario_id=? ORDER BY data_hora DESC LIMIT 5", (uid,)).fetchall()
        print(f"User {uid} - {name}: registros last30={count30}, last5={[ (r['data_hora'], r['tipo']) for r in last5 ]}")
    # Search for horas JS arrays in HTML
    if 'let horasSemana=' in html:
        idx = html.find('let horasSemana=')
        snippet = html[idx: idx+500]
        print('\nFound horasSemana JS snippet:')
        print(snippet)
    else:
        print('\nNo horasSemana variable found in HTML')
    if 'let horas_mes=' in html or 'let horasMes' in html:
        print('Found monthly hours variable in HTML')
    conn.close()
except Exception as e:
    print('Error reading DB:', e)
    sys.exit(0)
print('\nDone')
