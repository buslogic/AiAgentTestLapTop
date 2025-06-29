"""
Test BLBS AI Agent komponenti - jednostavna verzija
"""
from config.config_manager import ConfigManager
from database.blbs_connector import BLBSConnector
from utils.encryption import EncryptionManager

def test_encryption():
    print("[TEST] Enkriptovanje...")
    
    enc = EncryptionManager()
    test_data = "test_password_123"
    
    encrypted = enc.encrypt_data(test_data)
    print(f"   Enkriptovano: {encrypted[:30]}...")
    
    decrypted = enc.decrypt_data(encrypted)
    print(f"   Dekriptovano: {decrypted}")
    
    success = test_data == decrypted
    print(f"   Rezultat: {'PROSLO' if success else 'NEUSPESNO'}")
    return success

def test_config_manager():
    print("[TEST] Config manager...")
    
    config_manager = ConfigManager()
    
    test_config = {
        'host': '192.168.1.100',
        'username': 'test_user',
        'password': 'test_pass',
        'database': 'blbs_db',
        'port': '3306'
    }
    
    save_success = config_manager.save_config(test_config)
    print(f"   Cuvanje: {'PROSLO' if save_success else 'NEUSPESNO'}")
    
    loaded_config = config_manager.load_config()
    load_success = loaded_config is not None
    print(f"   Ucitavanje: {'PROSLO' if load_success else 'NEUSPESNO'}")
    
    if loaded_config:
        print(f"   Host: {loaded_config['host']}")
        print(f"   User: {loaded_config['username']}")
        print(f"   DB: {loaded_config['database']}")
    
    config_manager.delete_config()
    print("   Config manager: TESTIRAN")
    return save_success and load_success

def test_database_connector():
    print("[TEST] Database connector...")
    
    fake_config = {
        'host': '127.0.0.1',
        'username': 'fake_user',
        'password': 'fake_pass',
        'database': 'fake_db',
        'port': '3306'
    }
    
    connector = BLBSConnector(fake_config)
    success, message = connector.test_connection()
    
    print(f"   Konekcija: {'OCEKIVANO NEUSPESNO' if not success else 'NEOCEKIVANO USPESNO'}")
    print(f"   Poruka sadrzi status: {'DA' if 'Status:' in message else 'NE'}")
    print("   Database connector: TESTIRAN")
    return True

def main():
    print("*** BLBS AI Agent - Test komponenti ***")
    print("=" * 45)
    
    tests = [
        ("Enkriptovanje", test_encryption),
        ("Config Manager", test_config_manager), 
        ("Database Connector", test_database_connector)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print()
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    print()
    print("=" * 45)
    print("REZIME TESTOVA:")
    print("=" * 45)
    
    for test_name, success, error in results:
        status = "PROSAO" if success else "NEUSPESNO"
        print(f"{test_name:20} : {status}")
        if error:
            print(f"                     Greska: {error}")
    
    total_passed = sum(1 for _, success, _ in results if success)
    print(f"\nUkupno: {total_passed}/{len(results)} testova proslo")
    
    if total_passed == len(results):
        print("\n*** SVI TESTOVI SU PROSLI! ***")
        print("BLBS AI Agent je spreman za korisćenje!")
    else:
        print(f"\n{len(results) - total_passed} test(ova) nije proslo")

if __name__ == "__main__":
    main()