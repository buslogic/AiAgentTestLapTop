"""
Glavni UI za BLBS AI Agent
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from config.config_manager import ConfigManager
from database.blbs_connector import BLBSConnector


class BLBSMainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLBS AI Agent")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Managers
        self.config_manager = ConfigManager()
        
        # Setup UI
        self.setup_ui()
        
        # Proveri da li je konfigurisan
        if not self.config_manager.is_configured():
            self.show_configuration_dialog()
    
    def setup_ui(self):
        """Kreira glavni UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="BLBS AI Agent", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Connection status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status konekcije", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, width=70)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        # Buttons
        ttk.Button(button_frame, text="Testiraj konekciju", 
                   command=self.test_connection).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Konfiguracija", 
                   command=self.show_configuration_dialog).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Obriši konfiguraciju", 
                   command=self.delete_configuration).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Izlaz", 
                   command=self.root.quit).pack(side=tk.RIGHT)
        
        # Initial status
        self.update_status("BLBS AI Agent pokrennut.\nKliknite 'Testiraj konekciju' za proveru statusa.")
    
    def show_configuration_dialog(self):
        """Prikazuje dijalog za konfiguraciju"""
        config_window = tk.Toplevel(self.root)
        config_window.title("BLBS Konfiguracija")
        config_window.geometry("400x300")
        config_window.resizable(False, False)
        
        # Make modal
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Center the window
        config_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, 
                                          self.root.winfo_rooty() + 100))
        
        # Configuration frame
        config_frame = ttk.Frame(config_window, padding="20")
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load existing config if available
        existing_config = self.config_manager.load_config() or {}
        
        # Input fields
        ttk.Label(config_frame, text="IP adresa/Host:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        host_var = tk.StringVar(value=existing_config.get('host', ''))
        host_entry = ttk.Entry(config_frame, textvariable=host_var, width=30)
        host_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(config_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        port_var = tk.StringVar(value=existing_config.get('port', '3306'))
        port_entry = ttk.Entry(config_frame, textvariable=port_var, width=30)
        port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(config_frame, text="Korisničko ime:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        username_var = tk.StringVar(value=existing_config.get('username', ''))
        username_entry = ttk.Entry(config_frame, textvariable=username_var, width=30)
        username_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(config_frame, text="Lozinka:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        password_var = tk.StringVar(value=existing_config.get('password', ''))
        password_entry = ttk.Entry(config_frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(config_frame, text="Naziv baze:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        database_var = tk.StringVar(value=existing_config.get('database', ''))
        database_entry = ttk.Entry(config_frame, textvariable=database_var, width=30)
        database_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Configure grid
        config_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        def save_config():
            config_data = {
                'host': host_var.get().strip(),
                'port': port_var.get().strip(),
                'username': username_var.get().strip(),
                'password': password_var.get(),
                'database': database_var.get().strip()
            }
            
            # Validation
            if not all([config_data['host'], config_data['username'], 
                       config_data['password'], config_data['database']]):
                messagebox.showerror("Greška", "Sva polja moraju biti popunjena!")
                return
            
            if self.config_manager.save_config(config_data):
                messagebox.showinfo("Uspeh", "Konfiguracija je sačuvana!")
                config_window.destroy()
                self.update_status("Konfiguracija je ažurirana. Kliknite 'Testiraj konekciju' za proveru.")
            else:
                messagebox.showerror("Greška", "Greška pri čuvanju konfiguracije!")
        
        ttk.Button(button_frame, text="Sačuvaj", command=save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Otkaži", command=config_window.destroy).pack(side=tk.LEFT)
        
        # Focus on first field
        host_entry.focus()
    
    def test_connection(self):
        """Testira konekciju sa bazom"""
        config = self.config_manager.load_config()
        if not config:
            messagebox.showwarning("Upozorenje", "Prvo konfigurisajte konekciju!")
            self.show_configuration_dialog()
            return
        
        self.update_status("Testiram konekciju...\n⏳ Molimo sačekajte...")
        
        # Run test in separate thread to avoid UI freezing
        def run_test():
            connector = BLBSConnector(config)
            success, message = connector.test_connection()
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_status(message))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def delete_configuration(self):
        """Briše konfiguraciju"""
        if messagebox.askyesno("Potvrda", "Da li ste sigurni da želite da obrišete konfiguraciju?"):
            if self.config_manager.delete_config():
                messagebox.showinfo("Uspeh", "Konfiguracija je obrisana!")
                self.update_status("Konfiguracija je obrisana.\nPotrebno je ponovo konfigurisati konekciju.")
            else:
                messagebox.showerror("Greška", "Greška pri brisanju konfiguracije!")
    
    def update_status(self, message: str):
        """Ažurira status tekst"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, message)
        self.status_text.see(tk.END)
    
    def run(self):
        """Pokretanje aplikacije"""
        self.root.mainloop()