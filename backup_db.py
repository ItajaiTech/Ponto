import shutil
from datetime import datetime

# Caminho do banco de dados
origem = 'ponto.db'
# Nome do backup com data/hora
backup = f"ponto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

shutil.copy2(origem, backup)
print(f'Backup criado: {backup}')
