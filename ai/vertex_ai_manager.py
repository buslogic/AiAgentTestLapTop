"""
Vertex AI Manager za Claude Sonnet 4 integraciju
"""
import os
import json
from typing import Dict, Optional, Tuple
import requests
from google.auth import default
from google.oauth2 import service_account
from google.auth.transport.requests import Request


class VertexAIManager:
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.credentials = None
        self.is_initialized = False
        self.model_name = "claude-sonnet-4@20250514"
    
    def initialize(self) -> Tuple[bool, str]:
        """Inicijalizuje Vertex AI sa konfiguraciju"""
        try:
            # Setup credentials sa potrebnim scope-ovima za Vertex AI
            scopes = [
                'https://www.googleapis.com/auth/cloud-platform'
            ]
            
            if self.config.get('service_account_path'):
                self.credentials = service_account.Credentials.from_service_account_file(
                    self.config['service_account_path'],
                    scopes=scopes
                )
            else:
                self.credentials, _ = default(scopes=scopes)
            
            # Refresh credentials ako je potrebno
            if not self.credentials.valid:
                self.credentials.refresh(Request())
            
            self.is_initialized = True
            
            success_message = f"""
✅ VERTEX AI USPEŠNO POVEZAN!

🚀 Projekat: {self.config['project_id']}
🌍 Region: {self.config.get('region', 'europe-west1')}
🤖 Model: {self.model_name}
🔑 Autentifikacija: {'Service Account' if self.config.get('service_account_path') else 'Default'}

Status: SPREMAN ZA KORIŠĆENJE ✅
"""
            return True, success_message
            
        except FileNotFoundError as e:
            error_message = f"""
❌ SERVICE ACCOUNT FAJL NIJE PRONAĐEN!

📁 Putanja: {self.config.get('service_account_path', 'N/A')}

Rešenje:
• Proverite da li je putanja tačna
• Proverite da li fajl postoji
• Proverite dozvole za čitanje fajla

Status: NIJE POVEZANO ❌
"""
            return False, error_message
            
        except Exception as e:
            error_str = str(e)
            
            # Specific error messages
            if "invalid_scope" in error_str:
                error_message = f"""
❌ OAUTH SCOPE GREŠKA!

Greška: {error_str}

Rešenja:
• Proverite da li Service Account ima "Vertex AI User" ulogu
• U Google Cloud Console idi na IAM & Admin
• Dodajte "Vertex AI User" ili "AI Platform Admin" ulogu
• Proverite da li je Vertex AI API aktiviran

Status: SCOPE PROBLEMA ❌
"""
            elif "FileNotFoundError" in error_str:
                error_message = f"""
❌ SERVICE ACCOUNT FAJL GREŠKA!

Putanja nije validna ili fajl ne postoji.

Rešenja:
• Proverite putanju do JSON fajla
• Proverite da li fajl postoji
• Koristite apsolutnu putanju (C:\\path\\to\\file.json)

Status: FAJL PROBLEMA ❌
"""
            else:
                error_message = f"""
❌ GREŠKA PRI POVEZIVANJU SA VERTEX AI!

Greška: {error_str}

Mogući uzroci:
• Pogrešan Project ID
• Vertex AI API nije aktiviran
• Neispravni kredencijali
• Service Account nema potrebne dozvole

Status: NIJE POVEZANO ❌
"""
            return False, error_message
    
    def _make_api_request(self, prompt: str) -> str:
        """Poziva Claude Sonnet 4 preko Vertex AI streamRawPredict API"""
        
        # Build endpoint URL
        project_id = self.config['project_id']
        region = self.config.get('region', 'europe-west1')
        
        if region == "global":
            endpoint = "https://aiplatform.googleapis.com"
        else:
            endpoint = f"https://{region}-aiplatform.googleapis.com"
        
        url = f"{endpoint}/v1/projects/{project_id}/locations/{region}/publishers/anthropic/models/{self.model_name}:streamRawPredict"
        
        # Prepare request body
        request_body = {
            "anthropic_version": "vertex-2023-10-16",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "stream": False
        }
        
        # Make request
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text']
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testira konekciju sa Vertex AI"""
        if not self.is_initialized:
            success, message = self.initialize()
            if not success:
                return False, message
        
        try:
            # Test simple prompt using streamRawPredict API
            test_prompt = "Odgovori kratko: Da li radiš?"
            response_text = self._make_api_request(test_prompt)
            
            test_message = f"""
✅ VERTEX AI TEST USPEŠAN!

🤖 Model: {self.model_name}
📝 Test pitanje: {test_prompt}
💬 Test odgovor: {response_text[:100]}...

Status: FUNKCIONALAN ✅
"""
            return True, test_message
            
        except Exception as e:
            error_message = f"""
❌ TEST NEUSPEŠAN!

Greška: {str(e)}

Status: PROBLEM SA MODELOM ❌
"""
            return False, error_message
    
    def generate_report(self, sql_data: str, report_type: str = "osnovni") -> Tuple[bool, str]:
        """Generiše izveštaj na osnovu BLBS podataka"""
        if not self.is_initialized:
            return False, "Vertex AI nije inicijalizovan!"
        
        try:
            prompt = f"""
Analiziraj sledeće podatke iz BLBS (BusLogic Ticketing System) baze podataka i napravi {report_type} izveštaj na srpskom jeziku:

PODACI:
{sql_data}

Molim te da napraviš strukturiran izveštaj koji sadrži:
1. Kratak pregled podataka
2. Ključne statistike
3. Trendove ili obrazce koji se uočavaju
4. Preporuke ili zaključke

Odgovori na srpskom jeziku koristeći latinično pismo.
"""
            
            response_text = self._make_api_request(prompt)
            return True, response_text
            
        except Exception as e:
            return False, f"Greška pri generisanju izveštaja: {str(e)}"
    
    def chat(self, message: str) -> Tuple[bool, str]:
        """Osnovni chat sa AI modelom"""
        if not self.is_initialized:
            return False, "Vertex AI nije inicijalizovan!"
        
        try:
            prompt = f"""
Odgovori na srpskom jeziku koristeći latinično pismo.

Pitanje: {message}
"""
            response_text = self._make_api_request(prompt)
            return True, response_text
            
        except Exception as e:
            return False, f"Greška u chat komunikaciji: {str(e)}"