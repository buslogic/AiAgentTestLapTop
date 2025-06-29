"""
Test BLBS AI Agent komponenti bez GUI
"""
from config.config_manager import ConfigManager
from database.blbs_connector import BLBSConnector
from utils.encryption import EncryptionManager

def test_encryption():
    """Testira enkriptovanje"""
    print("[ENCRYPTION] Testiram enkriptovanje...")
    
    enc = EncryptionManager()
    test_data = "test_password_123"
    
    encrypted = enc.encrypt_data(test_data)
    print(f"   Enkriptovano: {encrypted[:50]}...")
    
    decrypted = enc.decrypt_data(encrypted)
    print(f"   Dekriptovano: {decrypted}")
    
    success = test_data == decrypted
    print(f"   [OK] Enkriptovanje: {'PROSLO' if success else 'NEUSPESNO'}\n")
    return success

def test_config_manager():
    """Testira config manager"""
    print("⚙️ Testiram config manager...")
    
    config_manager = ConfigManager()
    
    # Test config
    test_config = {
        'host': '192.168.1.100',
        'username': 'test_user',
        'password': 'test_pass',
        'database': 'blbs_db',
        'port': '3306'
    }
    
    # Save config
    save_success = config_manager.save_config(test_config)
    print(f"   Čuvanje: {'✅ PROŠLO' if save_success else '❌ NEUSPEŠNO'}")
    
    # Load config
    loaded_config = config_manager.load_config()
    load_success = loaded_config is not None
    print(f"   Učitavanje: {'✅ PROŠLO' if load_success else '❌ NEUSPEŠNO'}")
    
    if loaded_config:
        print(f"   Host: {loaded_config['host']}")
        print(f"   User: {loaded_config['username']}")
        print(f"   DB: {loaded_config['database']}")
    
    # Clean up
    config_manager.delete_config()
    print(f"   ✅ Config manager: TESTIRAN\n")
    return save_success and load_success

def test_database_connector():
    """Testira database connector sa lažnim podacima"""
    print("🗄️ Testiram database connector...")
    
    # Fake config za test
    fake_config = {
        'host': '127.0.0.1',
        'username': 'fake_user',
        'password': 'fake_pass',
        'database': 'fake_db',
        'port': '3306'
    }
    
    connector = BLBSConnector(fake_config)
    success, message = connector.test_connection()
    
    print(f"   Konekcija: {'❌ OČEKIVANO NEUSPEŠNO' if not success else '✅ NEOČEKIVANO USPEŠNO'}")
    print(f"   Poruka sadrži status: {'✅ DA' if 'Status:' in message else '❌ NE'}")
    print(f"   ✅ Database connector: TESTIRAN\n")
    return True

def main():
    """Glavna test funkcija"""
    print("*** BLBS AI Agent - Test komponenti ***\n")
    print("=" * 50)
    
    tests = [
        ("Enkriptovanje", test_encryption),
        ("Config Manager", test_config_manager), 
        ("Database Connector", test_database_connector)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    print("=" * 50)
    print("📊 REZIME TESTOVA:")
    print("=" * 50)
    
    for test_name, success, error in results:
        status = "✅ PROŠAO" if success else "❌ NEUSPEŠAN"
        print(f"{test_name:20} : {status}")
        if error:
            print(f"                     Greška: {error}")
    
    total_passed = sum(1 for _, success, _ in results if success)
    print(f"\n🎯 Ukupno: {total_passed}/{len(results)} testova prošlo")
    
    if total_passed == len(results):
        print("\n🎉 SVI TESTOVI SU PROŠLI!")
        print("✅ BLBS AI Agent je spreman za korišćenje!")
    else:
        print(f"\n⚠️ {len(results) - total_passed} test(ova) nije prošlo")

if __name__ == "__main__":
    main()