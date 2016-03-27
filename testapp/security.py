import os
from passlib.apps import custom_app_context as pwd_context


def check_pw(pw):
    """Check Password."""
    hashed = pwd_context.encrypt(os.environ.get('AUTH_PASSWORD', 'secret'))
    return pwd_context.verify(pw, hashed)
