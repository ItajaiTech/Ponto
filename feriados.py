from datetime import datetime
import requests
# Lista de feriados nacionais fixos (pode ser expandida ou lida de arquivo futuramente)
# Lista de feriados nacionais fixos (pode ser expandida ou lida de arquivo futuramente)
FERIADOS_FIXOS = [
    (1, 1),    # Confraternização Universal
    (4, 21),   # Tiradentes
    (5, 1),    # Dia do Trabalho
    (9, 7),    # Independência do Brasil
    (10, 12),  # Nossa Senhora Aparecida
    (11, 2),   # Finados
    (11, 15),  # Proclamação da República
    (12, 25),  # Natal
]

def obter_feriados_brasilapi(ano=None, estado=None, cidade=None):
    """
    Busca feriados nacionais, estaduais ou municipais do Brasil para o ano informado usando BrasilAPI.
    Retorna lista de tuplas (mes, dia).
    estado: sigla do estado (ex: 'PR', 'SC')
    cidade: nome da cidade (ex: 'foz do iguacu', 'itajai')
    """
    if ano is None:
        from datetime import datetime
        ano = datetime.now().year
    url = f'https://brasilapi.com.br/api/feriados/v1/{ano}'
    params = {}
    if estado:
        params['estado'] = estado.upper()
    if cidade:
        params['cidade'] = cidade.lower().replace(' ', '-')
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        feriados = resp.json()
        return [(int(f['date'][5:7]), int(f['date'][8:10])) for f in feriados]
    except Exception as e:
        print(f"Erro ao buscar feriados na BrasilAPI: {e}")
        return []

def is_feriado(data):
    """
    Verifica se a data é feriado nacional fixo.
    data: datetime.date ou datetime
    """
    if isinstance(data, datetime):
        data = data.date()
    return (data.month, data.day) in FERIADOS_FIXOS
