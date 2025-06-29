"""
Menadžer konfiguracije za BLBS AI Agent
"""
import json
import os
from typing import Dict, Optional
from utils.encryption import EncryptionManager


class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'blbs_config.json')
        self.encryption = EncryptionManager()
    
    def save_config(self, config_data: Dict[str, str]) -> bool:
        """Čuva konfiguraciju u enkriptovanom obliku"""
        try:
            # Enkriptuj osetljive podatke
            encrypted_config = {
                'host': self.encryption.encrypt_data(config_data.get('host', '')),
                'username': self.encryption.encrypt_data(config_data.get('username', '')),
                'password': self.encryption.encrypt_data(config_data.get('password', '')),
                'database': self.encryption.encrypt_data(config_data.get('database', '')),
                'port': config_data.get('port', '3306'),  # Port ne mora biti enkriptovan
                'configured': True
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Greška pri čuvanju konfiguracije: {e}")
            return False
    
    def load_config(self) -> Optional[Dict[str, str]]:
        """Učitava i dekriptuje konfiguraciju"""
        if not os.path.exists(self.config_file):
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                encrypted_config = json.load(f)
            
            if not encrypted_config.get('configured', False):
                return None
            
            # Dekriptuj podatke
            config = {
                'host': self.encryption.decrypt_data(encrypted_config['host']),
                'username': self.encryption.decrypt_data(encrypted_config['username']),
                'password': self.encryption.decrypt_data(encrypted_config['password']),
                'database': self.encryption.decrypt_data(encrypted_config['database']),
                'port': encrypted_config.get('port', '3306')
            }
            
            return config
        except Exception as e:
            print(f"Greška pri učitavanju konfiguracije: {e}")
            return None
    
    def is_configured(self) -> bool:
        """Proverava da li je konfiguracija postavljena"""
        return self.load_config() is not None
    
    def delete_config(self) -> bool:
        """Briše konfiguraciju"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            print(f"Greška pri brisanju konfiguracije: {e}")
            return False