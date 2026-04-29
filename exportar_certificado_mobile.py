#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para exportar certificado SSL em formato PKCS12 (.p12)
Para uso em dispositivos móveis (celular, tablet)
"""

import os
import sys
from pathlib import Path

def exportar_com_openssl():
    """
    Usa openssl.exe do sistema para criar PKCS12
    """
    
    certs_dir = Path(__file__).parent / 'certs'
    cert_file = certs_dir / 'ponto.crt'
    key_file = certs_dir / 'ponto.key'
    output_file = Path(__file__).parent / 'ponto_mobile.p12'
    
    # Comando OpenSSL
    cmd = f'openssl pkcs12 -export -in "{cert_file}" -inkey "{key_file}" -out "{output_file}" -name "PontoPro" -passout pass:'
    
    print("=" * 70)
    print("EXPORTANDO CERTIFICADO PARA DISPOSITIVOS MÓVEIS")
    print("=" * 70)
    print()
    
    # Verificar se os arquivos existem
    if not cert_file.exists():
        print(f"[✗] Certificado não encontrado: {cert_file}")
        return False
    
    if not key_file.exists():
        print(f"[✗] Chave privada não encontrado: {key_file}")
        return False
    
    print(f"[✓] Certificado encontrado: {cert_file}")
    print(f"[✓] Chave privada encontrado: {key_file}")
    print()
    
    # Tentar com openssl se disponível
    try:
        print("[*] Tentando usar OpenSSL do sistema...")
        resultado = os.system(cmd)
        
        if resultado == 0 and output_file.exists():
            tamanho = output_file.stat().st_size
            print(f"[✓] Certificado PKCS12 exportado com sucesso!")
            print(f"    Arquivo: {output_file}")
            print(f"    Tamanho: {tamanho} bytes")
            print()
            return True
        else:
            print("[!] OpenSSL pode não estar disponível.")
            return False
            
    except Exception as e:
        print(f"[!] Erro: {e}")
        return False


def exportar_direto():
    """
    Exporta arquivo único contendo certificado + chave (formato privado)
    """
    
    certs_dir = Path(__file__).parent / 'certs'
    cert_file = certs_dir / 'ponto.crt'
    key_file = certs_dir / 'ponto.key'
    
    output_file = Path(__file__).parent / 'ponto_mobile_combined.pem'
    
    try:
        # Combinar certificado e chave em um arquivo PEM
        with open(output_file, 'w') as dst:
            # Copiar chave
            with open(key_file, 'r') as src:
                dst.write(src.read())
            
            # Copiar certificado  
            with open(cert_file, 'r') as src:
                dst.write(src.read())
        
        tamanho = output_file.stat().st_size
        print(f"\n[✓] Arquivo PEM combinado exportado:")
        print(f"    Arquivo: {output_file}")
        print(f"    Tamanho: {tamanho} bytes")
        print(f"    (Contém chave privada + certificado)")
        return True
        
    except Exception as e:
        print(f"[!] Erro ao exportar PEM: {e}")
        return False


def exportar_pem_separado():
    """
    Exporta certificado e chave separados (formato PEM)
    """
    
    certs_dir = Path(__file__).parent / 'certs'
    cert_file = certs_dir / 'ponto.crt'
    key_file = certs_dir / 'ponto.key'
    
    output_cert = Path(__file__).parent / 'ponto_mobile.crt'
    output_key = Path(__file__).parent / 'ponto_mobile.key'
    
    try:
        # Copiar certificado
        with open(cert_file, 'rb') as src:
            with open(output_cert, 'wb') as dst:
                dst.write(src.read())
        
        # Copiar chave
        with open(key_file, 'rb') as src:
            with open(output_key, 'wb') as dst:
                dst.write(src.read())
        
        print(f"\n[✓] Arquivos PEM separados exportados:")
        print(f"    Certificado: {output_cert}")
        print(f"    Chave: {output_key}")
        return True
        
    except Exception as e:
        print(f"[!] Erro ao exportar PEM: {e}")
        return False


# ====================================================================

if __name__ == '__main__':
    
    print()
    
    # Tentar primeiro com OpenSSL (melhor formato)
    sucesso = exportar_com_openssl()
    
    # Se falhar, exportar em formatos alternativos
    if not sucesso:
        print()
        print("[*] Exportando em formatos alternativos...")
        exportar_direto()
    
    exportar_pem_separado()
    
    print()
    print("=" * 70)
    print("INSTRUÇOES DE USO NO CELULAR:")
    print("=" * 70)
    print()
    
    if sucesso:
        print("ARQUIVO PRINCIPAL: ponto_mobile.p12")
        print()
        print("1. TRANSFERIR ARQUIVO:")
        print("   - Caminho: C:\\RelogioPonto\\ponto_mobile.p12")
        print("   - Via: Email, WhatsApp, Pendrive, Nuvem, etc.")
        print()
        
        print("2. NO CELULAR (Android):")
        print("   a) Abra o gerenciador de arquivos")
        print("   b) Localize o arquivo ponto_mobile.p12")
        print("   c) Toque nele para abrir")
        print("   d) Sistema perguntará sobre instalação")
        print("   e) Selecione 'Armazenamento de credenciais'")
        print("   f) Certificado será instalado")
        print()
        
        print("3. NO CELULAR (iOS/iPad):")
        print("   a) Envie arquivo por email")
        print("   b) Abra o email no celular")
        print("   c) Toque no arquivo ponto_mobile.p12")
        print("   d) Clique em 'Mais' > 'Carregar em Configurações'")
        print("   e) Selecione 'Perfil de VPN e Dispositivo'")
        print("   f) Digite a senha (deixe em branco se sem senha)")
        print("   g) Certificado será instalado")
        print()
    else:
        print("ARQUIVOS ALTERNATIVOS:")
        print("  - ponto_mobile_combined.pem (chave + certificado combinados)")
        print("  - ponto_mobile.crt (certificado)")
        print("  - ponto_mobile.key (chave privada)")
        print()
    
    print("4. ACESSAR NO NAVEGADOR DO CELULAR:")
    print("   - URL: https://ponto.admin:5050")
    print("   - Ou: https://ponto.local:5050")
    print()
    
    print("5. CREDENCIAIS LOGIN:")
    print("   - CPF: 00000000000")
    print("   - Senha: Pont0!2024@Admin#Secure")
    print()
    
    print("6. AVISO DE CERTIFICADO:")
    print("   ⚠ Este é um certificado auto-sinado")
    print("   ⚠ Navegadores podem mostrar avisos de segurança")
    print("   ⚠ Clique em continuar/aceitar para prosseguir")
    print("   ⚠ Isso é normal e esperado")
    print()
    
    print("=" * 70)
    print("✓ Exportação concluída!")
    print("=" * 70)
    print()
    print(f"Arquivos disponíveis em: C:\\RelogioPonto\\")
    
    # Verificar se os arquivos existem
    if not cert_file.exists():
        print(f"[✗] Certificado não encontrado: {cert_file}")
        return False
    
    if not key_file.exists():
        print(f"[✗] Chave privada não encontrada: {key_file}")
        return False
    
    print(f"[✓] Certificado encontrado: {cert_file}")
    print(f"[✓] Chave privada encontrada: {key_file}")
    print()
    
    try:
        # Ler certificado
        with open(cert_file, 'rb') as f:
            cert_data = f.read()
        
        # Ler chave privada
        with open(key_file, 'rb') as f:
            key_data = f.read()
        
        # Carregar certificado
        cert = x509.load_pem_x509_certificate(
            cert_data,
            backend=default_backend()
        )
        
        # Carregar chave privada
        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=default_backend()
        )
        
        # Exportar em formato PKCS12
        # Nota: sem senha para facilitar instalação em celular
        pkcs12_data = serialization.pkcs12.serialize_key_and_certificates(
            name=b'Certificado-PontoPro',
            key=private_key,
            cert=cert,
            cas=[],  # Sem certificados intermediários
            friendly_name=b'RelogioPonto - PontoPro',
            encryption_algorithm=serialization.NoEncryption()  # Sem senha
        )
        
        # Salvar arquivo
        with open(output_file, 'wb') as f:
            f.write(pkcs12_data)
        
        print(f"[✓] Certificado PKCS12 exportado com sucesso!")
        print(f"    Arquivo: {output_file}")
        print(f"    Tamanho: {len(pkcs12_data)} bytes")
        print()
        
        # Obter informações do certificado
        subject = cert.subject.get_attributes_for_oid(cert.subject.oid)[0].value if cert.subject else "N/A"
        valid_from = cert.not_valid_before
        valid_to = cert.not_valid_after
        
        print("INFORMAÇÕES DO CERTIFICADO:")
        print(f"  Validade: {valid_from.strftime('%d/%m/%Y')} até {valid_to.strftime('%d/%m/%Y')}")
        print()
        
        return True
        
    except Exception as e:
        print(f"[✗] Erro ao exportar: {e}")
        import traceback
        traceback.print_exc()
        return False

def exportar_certificado_pem():
    """
    Também exporta em formato PEM separado (opcional)
    """
    
    certs_dir = Path(__file__).parent / 'certs'
    cert_file = certs_dir / 'ponto.crt'
    key_file = certs_dir / 'ponto.key'
    
    output_cert = Path(__file__).parent / 'ponto_mobile.crt'
    output_key = Path(__file__).parent / 'ponto_mobile.key'
    
    try:
        # Copiar certificado
        with open(cert_file, 'rb') as src:
            with open(output_cert, 'wb') as dst:
                dst.write(src.read())
        
        # Copiar chave
        with open(key_file, 'rb') as src:
            with open(output_key, 'wb') as dst:
                dst.write(src.read())
        
        print("FORMATOS ALTERNATIVOS (PEM):")
        print(f"  Certificado: {output_cert}")
        print(f"  Chave: {output_key}")
        print()
        
        return True
    except Exception as e:
        print(f"[!] Erro ao exportar PEM: {e}")
        return False

# ====================================================================

if __name__ == '__main__':
    
    sucesso_p12 = exportar_certificado_p12()
    print()
    sucesso_pem = exportar_certificado_pem()
    
    if sucesso_p12:
        print("=" * 70)
        print("INSTRUÇOES DE USO NO CELULAR:")
        print("=" * 70)
        print()
        print("1. TRANSFERIR ARQUIVO:")
        print("   - Caminho: C:\\RelogioPonto\\ponto_mobile.p12")
        print("   - Via: Email, WhatsApp, Pendrive, ou Nuvem")
        print()
        
        print("2. NO CELULAR (Android):")
        print("   a) Abra o arquivo ponto_mobile.p12")
        print("   b) Sistema perguntará sobre nome e armazenamento")
        print("   c) Selecione 'Armazenamento de credenciais'")
        print("   d) Certificado será instalado")
        print()
        
        print("3. NO CELULAR (iOS):")
        print("   a) Abra o arquivo ponto_mobile.p12")
        print("   b) Clique em 'Mais' > 'Adicionar'")
        print("   c) Selecione 'Perfil de VPN e Dispositivo'")
        print("   d) Insira senha (sem senha aqui)")
        print("   e) Certificado será instalado")
        print()
        
        print("4. ACESSAR NO NAVEGADOR DO CELULAR:")
        print("   - URL: https://ponto.admin:5050")
        print("   - Sistema usará certificado instalado")
        print("   - Login: 00000000000 / Pont0!2024@Admin#Secure")
        print()
        
        print("5. AVISO IMPORTANTE:")
        print("   ⚠ Este é um certificado auto-sinado")
        print("   ⚠ Navegadores podem mostrar warnings")
        print("   ⚠ Clique em continuar/aceitar")
        print()
        
        print("=" * 70)
        print("✓ Exportação concluída com sucesso!")
        print("=" * 70)
    else:
        print("[✗] Falha na exportação. Verifique os arquivos de certificado.")
