import hashlib
import secrets

# Funkcja do haszowania hasła przy użyciu SHA256
def hash_password_sha256(password: str) -> str:
    # Tworzymy hash przy użyciu SHA256
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return sha256_hash

# Funkcja do generowania 64 znakowego API
def generate_api_key():
    return secrets.token_hex(32)
