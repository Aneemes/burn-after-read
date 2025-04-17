# utils.py
import os
from cryptography.fernet import Fernet

def get_or_create_key():
    key_path = os.path.join(os.path.dirname(__file__), 'encryption.key')
    if os.path.exists(key_path):
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        return key

