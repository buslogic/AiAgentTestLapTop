"""
Debug verzija aplikacije da vidimo greške
"""
import sys
import os
import traceback

# Dodaj project root u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Pokušavam import...")
    from ui.tabbed_main_window import BLBSTabbedMainWindow
    print("Import uspešan!")
    
    print("Kreiram aplikaciju...")
    app = BLBSTabbedMainWindow()
    print("Aplikacija kreirana!")
    
    print("Pokretam GUI...")
    app.run()
    print("GUI završen!")
    
except Exception as e:
    print(f"\n❌ GREŠKA:")
    print(f"Tip: {type(e).__name__}")
    print(f"Poruka: {str(e)}")
    print(f"\n📋 DETALJAN TRACEBACK:")
    traceback.print_exc()
    
    input("\nPritisnite Enter za izlaz...")
except KeyboardInterrupt:
    print("\nAplikacija prekinuta od strane korisnika")