#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste direto do app.py para verificar as mudanças
"""
import re

print("Verificando código em app.py...\n")

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Procurar pelas mudanças
print("1. Verificando formatação coluna L (H.N.):")
if "hn_cell.number_format = 'hh:mm:ss'" in content:
    print("   ✅ Formato 'hh:mm:ss' aplicado a H.N.")
else:
    if "hn_cell.number_format = '[h]:mm:ss'" in content:
        print("   ⚠️  Formato '[h]:mm:ss' encontrado (deve ser 'hh:mm:ss')")
    else:
        print("   ❌ Formato não encontrado em H.N.")

print("\n2. Verificando formatação coluna M (H.E.):")
if "he_cell.number_format = 'hh:mm:ss'" in content:
    print("   ✅ Formato 'hh:mm:ss' aplicado a H.E.")
else:
    if "he_cell.number_format = '[h]:mm:ss'" in content:
        print("   ⚠️  Formato '[h]:mm:ss' encontrado (deve ser 'hh:mm:ss')")
    else:
        print("   ❌ Formato não encontrado em H.E.")

print("\n3. Verificando Jornada em sábado/domingo:")
if "if data.weekday() < 5:" in content:
    print("   ✅ Lógica corrigida: data.weekday() < 5")
    if "jornada_cell.number_format = 'hh:mm:ss'" in content:
        print("   ✅ Formato 'hh:mm:ss' aplicado à Jornada")
    else:
        print("   ⚠️  Formato não aplicado à Jornada")
else:
    print("   ⚠️  Lógica antiga encontrada")

print("\n4. Validando sintaxe Python:")
try:
    compile(content, 'app.py', 'exec')
    print("   ✅ Sintaxe válida")
except SyntaxError as e:
    print(f"   ❌ Erro: {e}")

print("\n✅ Verificação concluída!")
