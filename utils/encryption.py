"""
Enkriptovanje i dekriptovanje osetljivih podataka
"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    def __init__(self, password: str = "blbs_default_key"):
        self.password = password.encode()
        self.salt = b'salt_1234567890'
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)
    
    def _generate_key(self):
        """Generiše ključ za enkriptovanje"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt_data(self, data: str) -> str:
        """Enkriptuje podatke"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Dekriptuje podatke"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Greška pri dekriptovanju: {e}")