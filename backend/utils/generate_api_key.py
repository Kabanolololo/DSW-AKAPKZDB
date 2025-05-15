import secrets

# Funkcja do generowania 64 znakowego API
def generate_api_key():
    return secrets.token_hex(32)