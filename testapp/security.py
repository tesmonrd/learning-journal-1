import os
from passlib.apps import custom_app_context as pwd_context

def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD', 'this is not a password')
    return pwd_context.verify(pw, hashed)