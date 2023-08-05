from hashlib import sha256
from django.conf import settings
import secrets


def generate_api_key():
    return secrets.token_urlsafe()


def hash_api_key(raw_api_key):
    return sha256((settings.SECRET_KEY + raw_api_key).encode()).hexdigest()
