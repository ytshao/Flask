
from passlib.apps import custom_app_context as pwd_context

def make_password(password):
    return pwd_context.encrypt(password)
