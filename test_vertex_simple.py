"""
Test Vertex AI komponenti - jednostavna verzija
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config.vertex_config_manager import VertexConfigManager
    print("[OK] Vertex config manager import - PROSAO")
except Exception as e:
    print(f"[ERROR] Vertex config manager import - NEUSPESNO: {e}")

try:
    # Test osnovni config manager
    vertex_config = VertexConfigManager()
    print("[OK] Vertex config manager kreiranje - PROSAO")
    
    # Test save/load
    test_config = {
        'project_id': 'test-project-123',
        'region': 'us-central1',
        'service_account_path': '/path/to/service-account.json'
    }
    
    save_result = vertex_config.save_config(test_config)
    print(f"[TEST] Config save: {'PROSAO' if save_result else 'NEUSPESNO'}")
    
    loaded_config = vertex_config.load_config()
    load_result = loaded_config is not None
    print(f"[TEST] Config load: {'PROSAO' if load_result else 'NEUSPESNO'}")
    
    if loaded_config:
        print(f"   Project ID: {loaded_config.get('project_id', 'N/A')}")
        print(f"   Region: {loaded_config.get('region', 'N/A')}")
    
    # Cleanup
    vertex_config.delete_config()
    print("[OK] Vertex config test zavrsen")
    
except Exception as e:
    print(f"[ERROR] Vertex config test - NEUSPESNO: {e}")

print("\n" + "="*40)
print("VERTEX AI KOMPONENTE TEST ZAVRSEN")
print("="*40)

# Note: Ne testiramo VertexAIManager jer zahteva prave Google Cloud kredencijale