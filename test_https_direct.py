#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testa se os endpoints HTTPS funcionam diretamente
"""
import urllib.request
import ssl

# Desabilitar verificação de certificado self-signed
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

endpoints = [
    "https://ponto.local:5000",
    "https://ponto.admin:5050",
    "https://127.0.0.1:5000",
    "https://127.0.0.1:5050",
]

print("=== Testando acesso direto HTTPS ===\n")

for endpoint in endpoints:
    try:
        req = urllib.request.Request(endpoint)
        with urllib.request.urlopen(req, context=ssl_context, timeout=5) as response:
            status = response.status
            print("URL: {}".format(endpoint))
            print("  Status: {} OK \u2713".format(status))
            print()
    except Exception as e:
        print("URL: {}".format(endpoint))
        print("  Status: ERRO - {}".format(str(e)[:80]))
        print()

print("Teste concluido!")
