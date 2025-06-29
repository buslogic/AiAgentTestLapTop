"""
BLBS AI Agent - Glavna aplikacija sa tab-ovima
"""
import sys
import os

# Dodaj project root u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.tabbed_main_window import BLBSTabbedMainWindow


def main():
    """Glavna funkcija"""
    try:
        app = BLBSTabbedMainWindow()
        app.run()
    except Exception as e:
        print(f"Greška pri pokretanju aplikacije: {e}")
        input("Pritisnite Enter za izlaz...")


if __name__ == "__main__":
    main()