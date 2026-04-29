import sqlite3
from datetime import datetime, timedelta
import calendar
import random

def gerar_batidas_inteligente():

    conn = sqlite3.connect('ponto.db')
    c = conn.cursor()

    # ===============================
    # IDENTIFICAR MÊS ANTERIOR
    # ===============================
    hoje = datetime.now()
    primeiro_dia_mes_atual = datetime(hoje.year, hoje.month, 1)
    ultimo_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)

    ano = ultimo_mes_anterior.year
    mes = ultimo_mes_anterior.month

    total_dias = calendar.monthrange(ano, mes)[1]

    print(f"\nGerando batidas para {mes:02d}/{ano}")

    # ===============================
    # BUSCAR FUNCIONÁRIOS CADASTRADOS
    # ===============================
    c.execute("SELECT id, nome FROM usuarios WHERE tipo='funcionario'")
    funcionarios = c.fetchall()

    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return

    print(f"{len(funcionarios)} funcionário(s) encontrado(s).")

    # ===============================
    # PARA CADA FUNCIONÁRIO
    # ===============================
    for user_id, nome in funcionarios:

        print(f"\nProcessando: {nome}")

        for dia in range(1, total_dias + 1):

            data_base = datetime(ano, mes, dia)

            # Ignorar sábado e domingo
            if data_base.weekday() >= 5:
                continue

            data_str = data_base.strftime("%d/%m/%Y")

            # ===============================
            # VERIFICAR SE JÁ EXISTE REGISTRO
            # ===============================
            c.execute("""
            SELECT COUNT(*) FROM registros
            WHERE usuario_id=? AND data_hora LIKE ?
            """, (user_id, f"%{data_str}%"))

            if c.fetchone()[0] > 0:
                continue  # já tem batida, pula

            # ===============================
            # DEFINIR TIPO DE DIA
            # ===============================
            tipo_dia = random.choice([
                "normal",
                "atraso",
                "hora_extra",
                "atraso_compensado"
            ])

            # ===============================
            # HORÁRIOS BASE
            # ===============================
            entrada = data_base.replace(hour=8, minute=0, second=0)
            saida_almoco = data_base.replace(hour=12, minute=0, second=0)
            retorno = data_base.replace(hour=13, minute=0, second=0)
            saida_final = data_base.replace(hour=18, minute=0, second=0)

            # ===============================
            # VARIAÇÕES
            # ===============================

            # atraso na entrada
            if tipo_dia in ["atraso", "atraso_compensado"]:
                entrada += timedelta(minutes=random.randint(5, 30))

            # atraso leve no retorno
            if random.random() < 0.3:
                retorno += timedelta(minutes=random.randint(3, 15))

            # hora extra
            if tipo_dia == "hora_extra":
                saida_final += timedelta(minutes=random.randint(20, 120))

            # compensação
            if tipo_dia == "atraso_compensado":
                saida_final += timedelta(minutes=random.randint(40, 90))

            # ===============================
            # INSERIR NO BANCO
            # ===============================
            batidas = [entrada, saida_almoco, retorno, saida_final]

            for batida in batidas:

                c.execute("""
                INSERT INTO registros (usuario_id, tipo, data_hora)
                VALUES (?, ?, ?)
                """, (
                    user_id,
                    "AUTO",
                    batida.strftime("%d/%m/%Y %H:%M:%S")
                ))

        print(f"Batidas geradas para {nome}")

    conn.commit()
    conn.close()

    print("\nProcesso concluído com sucesso!")

# ===============================
if __name__ == "__main__":
    gerar_batidas_inteligente()
