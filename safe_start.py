"""
Bezbedan start aplikacije sa detaljnim error handling-om
"""
import sys
import os
import traceback
import tkinter as tk

# Dodaj project root u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testira sve import-e korak po korak"""
    try:
        print("1. Testiram osnovne import-e...")
        import tkinter
        print("   [OK] tkinter OK")
        
        print("2. Testiram naše module...")
        from config.config_manager import ConfigManager
        print("   [OK] ConfigManager OK")
        
        from config.vertex_config_manager import VertexConfigManager  
        print("   [OK] VertexConfigManager OK")
        
        from database.blbs_connector import BLBSConnector
        print("   [OK] BLBSConnector OK")
        
        print("3. Testiram Vertex AI (može da bude sporije)...")
        try:
            from ai.vertex_ai_manager import VertexAIManager
            print("   [OK] VertexAIManager OK")
        except Exception as e:
            print(f"   ⚠ VertexAIManager PROBLEM: {e}")
            return False
        
        print("4. Testiram glavnu UI klasu...")
        from ui.tabbed_main_window import BLBSTabbedMainWindow
        print("   [OK] BLBSTabbedMainWindow OK")
        
        return True
        
    except Exception as e:
        print(f"\n❌ IMPORT GREŠKA:")
        print(f"Tip: {type(e).__name__}")
        print(f"Poruka: {str(e)}")
        traceback.print_exc()
        return False

def test_basic_gui():
    """Testira osnovni Tkinter"""
    try:
        print("\n5. Testiram osnovni Tkinter GUI...")
        root = tk.Tk()
        root.title("Test")
        root.geometry("300x200")
        
        label = tk.Label(root, text="Test GUI - zatvorite ovaj prozor")
        label.pack(expand=True)
        
        print("   [OK] Osnovni GUI kreiran - zatvorite test prozor da nastavimo")
        root.mainloop()
        print("   [OK] Test GUI zatvoren")
        return True
        
    except Exception as e:
        print(f"\n❌ GUI GREŠKA: {e}")
        return False

def start_main_app():
    """Pokretanje glavne aplikacije"""
    try:
        print("\n6. Pokretam glavnu aplikaciju...")
        from ui.tabbed_main_window import BLBSTabbedMainWindow
        
        app = BLBSTabbedMainWindow()
        print("   [OK] Aplikacija kreirana")
        
        print("   → Pokretam GUI (aplikacija će se otvoriti)...")
        app.run()
        print("   [OK] Aplikacija zatvorena normalno")
        
    except Exception as e:
        print(f"\n❌ GLAVNA APLIKACIJA GREŠKA:")
        print(f"Tip: {type(e).__name__}")
        print(f"Poruka: {str(e)}")
        traceback.print_exc()

def main():
    """Glavna funkcija sa step-by-step testiranjem"""
    print("*** BLBS AI Agent - Bezbedan start ***")
    print("=" * 50)
    
    # Test import-a
    if not test_imports():
        print("\n❌ Import-ovi ne rade - aplikacija ne može da se pokrene")
        input("Pritisnite Enter za izlaz...")
        return
    
    print("\n[SUCCESS] Svi import-ovi uspesni!")
    
    # Test osnovnog GUI-ja
    if not test_basic_gui():
        print("\n❌ Osnovni GUI ne radi")
        input("Pritisnite Enter za izlaz...")
        return
    
    print("\n[SUCCESS] GUI testiranje uspesno!")
    
    # Pokreni glavnu aplikaciju
    start_main_app()
    
    print("\n[SUCCESS] Program zavrsen")

if __name__ == "__main__":
    main()