#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verificar se as mudanças foram aplicadas ao código
"""
import re

print("Verificando mudanças aplicadas ao app.py...\n")

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Verificação 1: Formato da coluna L (H.N.)
print("1. Verificando formato hora coluna L (H.N.)...")
if "hn_cell.number_format = '[h]:mm:ss'" in content:
    print("   ✅ Formato hora aplicado à coluna L (H.N.)")
else:
    print("   ❌ Formato hora NÃO encontrado em coluna L")

# Verificação 2: Formato da coluna M (H.E.)
print("\n2. Verificando formato hora coluna M (H.E.)...")
if "he_cell.number_format = '[h]:mm:ss'" in content:
    print("   ✅ Formato hora aplicado à coluna M (H.E.)")
else:
    print("   ❌ Formato hora NÃO encontrado em coluna M")

# Verificação 3: Verificar se Jornada não é preenchida em fim de semana
print("\n3. Verificando se Jornada é vazia em finais de semana...")
# Procurar por padrão que indique verificação de weekday em coluna K
if "is_weekend = data.weekday() in (5, 6)" in content:
    print("   ✅ Verificação de fim de semana encontrada")
    if "jornada_cell.value = '09:00:00'" in content:
        print("   ✅ Jornada preenchida apenas em dias úteis")
    else:
        print("   ❌ Lógica de preenchimento não encontrada")
else:
    # Verificar alternativa
    if "data.weekday() not in (5, 6)" in content:
        print("   ✅ Verificação de fim de semana encontrada (versão alternativa)")
    else:
        print("   ❌ Verificação de fim de semana NÃO encontrada")

# Verificação 4: Checar se as linhas não têm sintaxe errada
print("\n4. Compilando Python para verificar sintaxe...")
try:
    compile(content, 'app.py', 'exec')
    print("   ✅ Sintaxe Python válida")
except SyntaxError as e:
    print(f"   ❌ Erro de sintaxe: {e}")

# Contar número de ocorrências das formatações
print("\n5. Contagem de formatações hora:")
count_hn = content.count("hn_cell.number_format = '[h]:mm:ss'")
count_he = content.count("he_cell.number_format = '[h]:mm:ss'")
print(f"   H.N. formatações: {count_hn}")
print(f"   H.E. formatações: {count_he}")

print("\n✅ Verificação concluída!")
