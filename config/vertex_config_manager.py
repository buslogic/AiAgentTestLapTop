"""
Vertex AI konfiguracija manager
"""
import json
import os
from typing import Dict, Optional
from utils.encryption import EncryptionManager


class VertexConfigManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'vertex_config.json')
        self.encryption = EncryptionManager()
    
    def save_config(self, config_data: Dict[str, str]) -> bool:
        """Čuva Vertex AI konfiguraciju"""
        try:
            encrypted_config = {
                'project_id': self.encryption.encrypt_data(config_data.get('project_id', '')),
                'region': config_data.get('region', 'europe-west1'),  # Region ne mora biti enkriptovan
                'service_account_path': self.encryption.encrypt_data(config_data.get('service_account_path', '')),
                'configured': True
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Greška pri čuvanju Vertex AI konfiguracije: {e}")
            return False
    
    def load_config(self) -> Optional[Dict[str, str]]:
        """Učitava Vertex AI konfiguraciju"""
        if not os.path.exists(self.config_file):
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                encrypted_config = json.load(f)
            
            if not encrypted_config.get('configured', False):
                return None
            
            config = {
                'project_id': self.encryption.decrypt_data(encrypted_config['project_id']),
                'region': encrypted_config.get('region', 'europe-west1'),
                'service_account_path': self.encryption.decrypt_data(encrypted_config['service_account_path'])
            }
            
            return config
        except Exception as e:
            print(f"Greška pri učitavanju Vertex AI konfiguracije: {e}")
            return None
    
    def is_configured(self) -> bool:
        """Proverava da li je Vertex AI konfigurisan"""
        return self.load_config() is not None
    
    def delete_config(self) -> bool:
        """Briše Vertex AI konfiguraciju"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            print(f"Greška pri brisanju Vertex AI konfiguracije: {e}")
            return False