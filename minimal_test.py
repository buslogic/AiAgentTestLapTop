"""
Minimalna verzija aplikacije za testiranje
"""
import tkinter as tk
from tkinter import ttk

def test_gui():
    root = tk.Tk()
    root.title("BLBS AI Agent - Test")
    root.geometry("600x400")
    
    # Notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Tab 1 - MySQL
    mysql_frame = ttk.Frame(notebook)
    notebook.add(mysql_frame, text="MySQL Test")
    ttk.Label(mysql_frame, text="MySQL konfiguracija - TEST", 
              font=("Arial", 14)).pack(pady=20)
    ttk.Button(mysql_frame, text="Test MySQL").pack(pady=10)
    
    # Tab 2 - Vertex AI  
    ai_frame = ttk.Frame(notebook)
    notebook.add(ai_frame, text="Vertex AI Test")
    ttk.Label(ai_frame, text="Vertex AI konfiguracija - TEST", 
              font=("Arial", 14)).pack(pady=20)
    ttk.Button(ai_frame, text="Test Vertex AI").pack(pady=10)
    
    # Status
    status_label = ttk.Label(root, text="Status: Test aplikacija pokrenuta")
    status_label.pack(side=tk.BOTTOM, pady=5)
    
    print("Minimalna aplikacija pokrenuta - zatvorite prozor kad testirate")
    root.mainloop()
    print("Test aplikacija zatvorena")

if __name__ == "__main__":
    try:
        test_gui()
    except Exception as e:
        print(f"Greska: {e}")
        input("Enter za izlaz...")