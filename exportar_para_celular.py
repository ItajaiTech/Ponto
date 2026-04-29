#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exporta certificado SSL para uso em celulares
"""

from pathlib import Path

certs_dir = Path(__file__).parent / 'certs'
cert_file = certs_dir / 'ponto.crt'
key_file = certs_dir / 'ponto.key'

output_cert = Path(__file__).parent / 'ponto_mobile.crt'
output_key = Path(__file__).parent / 'ponto_mobile.key'
output_combined = Path(__file__).parent / 'ponto_mobile_complete.pem'

print("=" * 70)
print("EXPORTANDO CERTIFICADO PARA DISPOSITIVOS MÓVEIS")
print("=" * 70)
print()

if not cert_file.exists() or not key_file.exists():
    print("[✗] Arquivos de certificado não encontrados!")
    exit(1)

print(f"[✓] Certificado encontrado: {cert_file}")
print(f"[✓] Chave privada encontrada: {key_file}")
print()

try:
    # Copiar certificado
    with open(cert_file, 'rb') as src:
        with open(output_cert, 'wb') as dst:
            dst.write(src.read())
    
    # Copiar chave
    with open(key_file, 'rb') as src:
        with open(output_key, 'wb') as dst:
            dst.write(src.read())
    
    # Combinar em um arquivo PEM (chave + certificado)
    with open(output_combined, 'w') as dst:
        # Primeiro a chave
        with open(key_file, 'r') as src:
            dst.write(src.read())
        # Depois o certificado
        with open(cert_file, 'r') as src:
            dst.write(src.read())
    
    print("[✓] Arquivos exportados com sucesso!")
    print()
    
    # Mostrar informações dos arquivos
    cert_size = output_cert.stat().st_size
    key_size = output_key.stat().st_size
    combined_size = output_combined.stat().st_size
    
    print("ARQUIVOS GERADOS:")
    print(f"  1. {output_cert.name} ({cert_size} bytes)")
    print(f"  2. {output_key.name} ({key_size} bytes)")
    print(f"  3. {output_combined.name} ({combined_size} bytes)")
    print()
    
    print("=" * 70)
    print("COMO USAR NO CELULAR")
    print("=" * 70)
    print()
    
    print("OPÇÃO 1: Arquivo Individual (Recomendado para simplicidade)")
    print("-" * 70)
    print("Arquivo: ponto_mobile_complete.pem")
    print()
    print("Android:")
    print("  1. Copie o arquivo para o celular")
    print("  2. Abra em um app de gerenciador de certificados")
    print("  3. Selecione 'Instalar certificado'")
    print("  4. Escolha 'Armazenamento de credenciais'")
    print()
    
    print("iOS/iPad:")
    print("  1. Envie por email ou Airdrop")
    print("  2. Abra o arquivo")
    print("  3. Vá para Configurações > Geral > VPN e Gerenciamento de Dispositivo")
    print("  4. Selecione o certificado e confirme")
    print()
    
    print("OPÇÃO 2: Arquivos Separados")
    print("-" * 70)
    print("Use se precisar instalar chave e certificado separadamente")
    print()
    
    print("=" * 70)
    print("ACESSAR NO NAVEGADOR DO CELULAR")
    print("=" * 70)
    print()
    print("URL: https://ponto.admin:5050")
    print("   Ou: https://ponto.local:5050")
    print()
    print("Credenciais:")
    print("  CPF: 00000000000")
    print("  Senha: Pont0!2024@Admin#Secure")
    print()
    
    print("=" * 70)
    print("IMPORTANTE")
    print("=" * 70)
    print()
    print("⚠ Este é um certificado AUTO-SINADO")
    print("⚠ O navegador mostrará um aviso de segurança")
    print("⚠ Clique em 'Continuar' ou 'Aceitar' para prosseguir")
    print("⚠ Isso é NORMAL e seguro neste contexto")
    print()
    
    print("Localização dos arquivos:")
    print(f"  C:\\RelogioPonto\\ponto_mobile*")
    print()
    
except Exception as e:
    print(f"[✗] Erro: {e}")
    import traceback
    traceback.print_exc()
