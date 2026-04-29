#!/usr/bin/env python3
"""
Gera certificados SSL autossinados para domínios locais
"""
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, UTC
from ipaddress import ip_address
import os

CERTS_DIR = r'C:\RelogioPonto\certs'
KEY_FILE = os.path.join(CERTS_DIR, 'ponto.key')
CERT_FILE = os.path.join(CERTS_DIR, 'ponto.crt')


def build_san_entries(domains):
    entries = []
    for domain in domains:
        value = str(domain).strip()
        if not value:
            continue
        try:
            entries.append(x509.IPAddress(ip_address(value)))
        except ValueError:
            entries.append(x509.DNSName(value))
    return entries

def generate_certificates(domains):
    """Gera certificado autossinado para os domínios especificados"""
    
    print(f"[*] Gerando certificado para: {', '.join(domains)}")
    
    # Gerar chave privada
    print("[1] Gerando chave privada (2048 bits)...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Preparar Subject/Issuer
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "RelogioPonto"),
        x509.NameAttribute(NameOID.COMMON_NAME, domains[0]),
    ])
    
    # Construir certificado
    print("[2] Construindo certificado X509...")
    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.public_key(private_key.public_key())
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    now = datetime.now(UTC)
    cert_builder = cert_builder.not_valid_before(now)
    cert_builder = cert_builder.not_valid_after(now + timedelta(days=365))
    
    # Adicionar SAN (Subject Alternative Name)
    cert_builder = cert_builder.add_extension(
        x509.SubjectAlternativeName(build_san_entries(domains)),
        critical=False,
    )
    
    # Assinar certificado
    print("[3] Assinando certificado (autossinado)...")
    certificate = cert_builder.sign(
        private_key, hashes.SHA256()
    )
    
    # Salvar chave privada
    print(f"[4] Salvando chave privada: {KEY_FILE}")
    with open(KEY_FILE, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Salvar certificado
    print(f"[5] Salvando certificado: {CERT_FILE}")
    with open(CERT_FILE, 'wb') as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))
    
    print("\n=== CERTIFICADO GERADO COM SUCESSO ===")
    print(f"Chave privada: {KEY_FILE}")
    print(f"Certificado:   {CERT_FILE}")
    print("Valido por: 365 dias")
    print(f"Domínios: {', '.join(domains)}")
    print("\n⚠️  IMPORTANTE:")
    print("1. Este é um certificado autossinado (não confiável por padrão)")
    print("2. Navegadores mostrarão aviso de segurança")
    print("3. No Flask, use: ssl_context=('ponto.crt', 'ponto.key')")

if __name__ == '__main__':
    domains = ['ponto.local', 'ponto.admin', 'localhost', '127.0.0.1']
    generate_certificates(domains)
