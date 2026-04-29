#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de porta 5050 com timeout maior
"""
import urllib.request
import ssl
import time

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

url = "https://127.0.0.1:5050"

print("Testando {} com timeout de 10 segundos...".format(url))

for i in range(3):
    print("\nTentativa {}:".format(i+1))
    start = time.time()
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            elapsed = time.time() - start
            print("  Sucesso! Status: {} (tempo: {:.2f}s)".format(response.status, elapsed))
    except Exception as e:
        elapsed = time.time() - start
        print("  Erro: {} (tempo: {:.2f}s)".format(str(e)[:60], elapsed))
    
    time.sleep(1)

print("\nTeste concluido!")
