#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testa se as requisições HTTP nas portas 6000/6050 são redirecionadas para HTTPS em 5000/5050
"""
import urllib.request
import urllib.error
import ssl

# Desabilitar verificação de certificado self-signed
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Endpoints de teste - HTTP com redirecionamento automático
endpoints = [
    ("http://127.0.0.1:6000", "HTTPS 127.0.0.1:5000"),
    ("http://127.0.0.1:6050", "HTTPS 127.0.0.1:5050"),
    ("http://ponto.local:6000", "HTTPS ponto.local:5000"),
    ("http://ponto.admin:6050", "HTTPS ponto.admin:5050"),
]

print("=== Testando redirecionamento HTTP -> HTTPS ===\n")

for endpoint, description in endpoints:
    try:
        # Criar request com follow_redirects
        req = urllib.request.Request(endpoint)
        
        # urllib não segue redirects automaticamente com HEAD, temos que usar GET
        with urllib.request.urlopen(req, context=ssl_context, timeout=3) as response:
            status = response.status
            final_url = response.geturl()
            print("Endpoint: {}".format(endpoint))
            print("  Descricao: {}".format(description))
            print("  Status final: {} OK".format(status))
            print("  URL final: {}".format(final_url))
            if final_url.startswith('https://'):
                print("  Status: ✓ Redirecionado para HTTPS!")
            else:
                print("  Status: ~ Sin redirect detectado")
            print()
            
    except urllib.error.HTTPError as e:
        # Isso pode acontecer se há redirect mas urllib não segue
        status = e.code
        location = e.headers.get('Location', 'N/A')
        print("Endpoint: {}".format(endpoint))
        print("  Descricao: {}".format(description))
        print("  Status: {} (Redirect)".format(status))
        print("  Location: {}".format(location))
        if location and location.startswith('https://'):
            print("  Status: ✓ Redirecionado para HTTPS!")
        print()
        
    except Exception as e:
        print("Endpoint: {}".format(endpoint))
        print("  Descricao: {}".format(description))
        print("  Status: ERRO - {}".format(str(e)[:100]))
        print()

print("\nNota: Use https://ponto.local:5000 e https://ponto.admin:5050 diretamente")
