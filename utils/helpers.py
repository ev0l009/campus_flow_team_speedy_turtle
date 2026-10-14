import secrets
import string

def generate_prefixed_id(preffix: str, length: int = 5):
    character_pool = string.ascii_letters + string.digits
    suffix = ''.join(secrets.choice(character_pool) for _ in range(length))
    return f"{preffix}_{suffix}"
