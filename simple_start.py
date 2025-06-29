"""
Jednostavan start aplikacije
"""
import sys
import os

# Dodaj project root u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Pokretam BLBS AI Agent...")
    from ui.tabbed_main_window import BLBSTabbedMainWindow
    
    app = BLBSTabbedMainWindow()
    print("Aplikacija kreirana - otvaraju se tab-ovi...")
    app.run()
    print("Aplikacija zatvorena")
    
except Exception as e:
    print(f"GRESKA: {e}")
    import traceback
    traceback.print_exc()
    input("Pritisnite Enter za izlaz...")