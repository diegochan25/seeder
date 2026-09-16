import secrets
import hashlib
import hmac
from app.config.settings import get_settings


settings = get_settings()

def randhex(strlen: int) -> str:
    return secrets.token_hex(strlen // 2 + 1)[:strlen]

def randbase64url(strlen: int) -> str:
    return secrets.token_urlsafe(3 * strlen // 4 + 1)[:strlen]

def sha256hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def sha256hmac(text: str, key: str | None = None) -> str:
    key = key or settings.secret_key
    return hmac.new(key.encode('utf-8'), text.encode('utf-8'), hashlib.sha256).hexdigest()

def sha256compare(text: str, hashed: str, key: str | None = None) -> bool:
    if key is None:
        hmac.compare_digest(sha256hash(text), hashed)
    return hmac.compare_digest(sha256hmac(text, key), hashed)