import os

def check_pw(pw):
    return pw == os.environ.get('AUTH_PASSWORD', 'this is not a password')
