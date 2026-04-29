#!/usr/bin/env python3
"""Testa acesso HTTPS aos domínios"""
import urllib.request
import ssl

# Ignorar aviso de certificado autossinado
ssl_context = ssl._create_unverified_context()

urls = [
    "https://ponto.local:5000",
    "https://ponto.admin:5050",
    "https://127.0.0.1:5000",
    "https://127.0.0.1:5050",
]

print("=== Testando acesso HTTPS ===\n")

for url in urls:
    try:
        print(f"Testando {url}...", end=" ")
        response = urllib.request.urlopen(url, context=ssl_context, timeout=5)
        print(f"✓ {response.status}")
    except Exception as e:
        print(f"✗ Erro: {e}")

print("\n✓ Todos os testes completados!")
