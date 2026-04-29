#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testa se as requisições HTTP são redirecionadas para HTTPS
"""
import urllib.request
import urllib.error
import ssl
import sys

# Desabilitar verificação de certificado self-signed
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

endpoints = [
    "http://ponto.local:5000",
    "http://ponto.admin:5050",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5050",
]

print("=== Testando redirecionamento HTTP -> HTTPS ===\n")

for endpoint in endpoints:
    try:
        req = urllib.request.Request(endpoint, method='HEAD')
        with urllib.request.urlopen(req, context=ssl_context, timeout=3) as response:
            # Se chegar aqui, conseguiu conexão
            status = response.status
            location = response.headers.get('Location', 'N/A')
            print("URL: {}".format(endpoint))
            print("  Status: {}".format(status))
            print("  Location (redirect): {}".format(location))
            if status in [301, 302, 303, 307, 308]:
                print("  Status: OK - Redirect detectado!")
            elif location and location.startswith('https://'):
                print("  Status: OK - Header Location para HTTPS!")
            else:
                print("  Status: AVISO - Sem redirect detectado")
            print()
    except urllib.error.HTTPError as e:
        # HTTPError é lançado em redirects (3xx)
        status = e.code
        location = e.headers.get('Location', 'N/A')
        print("URL: {}".format(endpoint))
        print("  Status: {} (HTTPError - pode ser redirect)".format(status))
        print("  Location: {}".format(location))
        if status in [301, 302, 303, 307, 308]:
            if location.startswith('https://'):
                print("  Status: OK - Redirect para HTTPS!")
            else:
                print("  AVISO: Redirect para: {}".format(location))
        print()
    except Exception as e:
        print("URL: {}".format(endpoint))
        print("  Status: ERRO - {}".format(str(e)))
        print()

print("Teste concluido!")
