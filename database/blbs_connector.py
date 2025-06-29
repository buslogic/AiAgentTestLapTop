"""
BLBS Database Connector - Konekcija sa MySQL bazom
"""
import pymysql
from typing import Dict, Tuple, Optional


class BLBSConnector:
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.connection = None
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testira konekciju sa bazom podataka"""
        try:
            # Pokušaj konekcije
            connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['username'],
                password=self.config['password'],
                database=self.config['database'],
                port=int(self.config['port']),
                charset='utf8mb4',
                connect_timeout=10
            )
            
            # Testiranje osnovnih SQL komandi
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.execute("SELECT DATABASE()")
                database = cursor.fetchone()
            
            connection.close()
            
            status_message = f"""
✅ KONEKCIJA USPEŠNA!

🔗 Host: {self.config['host']}:{self.config['port']}
🗄️ Baza podataka: {self.config['database']}
👤 Korisnik: {self.config['username']}
🔧 MySQL verzija: {version[0] if version else 'N/A'}

Status: POVEZANO ✅
"""
            return True, status_message
            
        except pymysql.MySQLError as e:
            error_message = f"""
❌ KONEKCIJA NEUSPEŠNA!

🔗 Host: {self.config['host']}:{self.config['port']}
🗄️ Baza podataka: {self.config['database']}
👤 Korisnik: {self.config['username']}

❌ MySQL Greška: {str(e)}

Mogući uzroci:
• Pogrešna IP adresa ili port
• Neispravni kredencijali
• Baza podataka ne postoji
• Firewall blokira konekciju
• MySQL server nije pokrennut

Status: NIJE POVEZANO ❌
"""
            return False, error_message
            
        except Exception as e:
            error_message = f"""
❌ OPŠTA GREŠKA!

Greška: {str(e)}

Status: GREŠKA ❌
"""
            return False, error_message
    
    def connect(self) -> bool:
        """Otvara konekciju sa bazom"""
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['username'],
                password=self.config['password'],
                database=self.config['database'],
                port=int(self.config['port']),
                charset='utf8mb4'
            )
            return True
        except Exception as e:
            print(f"Greška pri konekciji: {e}")
            return False
    
    def disconnect(self):
        """Zatvara konekciju"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str) -> Optional[list]:
        """Izvršava SQL upit"""
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            return None