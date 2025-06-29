"""
BLBS AI Agent - Glavni fajl
"""
import sys
import os

# Dodaj project root u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import BLBSMainWindow


def main():
    """Glavna funkcija"""
    try:
        app = BLBSMainWindow()
        app.run()
    except Exception as e:
        print(f"Greška pri pokretanju aplikacije: {e}")
        input("Pritisnite Enter za izlaz...")


if __name__ == "__main__":
    main()