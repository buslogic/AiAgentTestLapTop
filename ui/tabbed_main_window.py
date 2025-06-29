"""
Prošireni glavni UI sa tab-ovima za BLBS AI Agent
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
from config.config_manager import ConfigManager
from config.vertex_config_manager import VertexConfigManager
from database.blbs_connector import BLBSConnector
from ai.vertex_ai_manager import VertexAIManager


class BLBSTabbedMainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLBS AI Agent - Proširena verzija")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Managers
        self.config_manager = ConfigManager()
        self.vertex_config_manager = VertexConfigManager()
        self.vertex_ai_manager = None
        
        # Setup UI
        self.setup_ui()
        
        # Proveri konfiguracije
        self.check_initial_setup()
    
    def setup_ui(self):
        """Kreira glavni UI sa tab-ovima"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="BLBS AI Agent", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_database_tab()
        self.create_vertex_ai_tab()
        self.create_reports_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Spreman")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_database_tab(self):
        """Kreira tab za database konfiguraciju"""
        db_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(db_frame, text="MySQL Baza")
        
        # Configure grid
        db_frame.columnconfigure(0, weight=1)
        db_frame.rowconfigure(1, weight=1)
        
        # Connection status frame
        status_frame = ttk.LabelFrame(db_frame, text="Status MySQL konekcije", padding="10")
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        
        self.db_status_text = scrolledtext.ScrolledText(status_frame, height=15, width=70)
        self.db_status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        db_button_frame = ttk.Frame(db_frame)
        db_button_frame.grid(row=1, column=0, pady=(10, 0), sticky=tk.W)
        
        ttk.Button(db_button_frame, text="Testiraj MySQL konekciju", 
                   command=self.test_database_connection).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(db_button_frame, text="MySQL konfiguracija", 
                   command=self.show_database_configuration).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(db_button_frame, text="Obriši MySQL config", 
                   command=self.delete_database_configuration).pack(side=tk.LEFT)
        
        # Initial status
        self.update_db_status("MySQL konfiguracija.\nKliknite 'MySQL konfiguracija' za setup.")
    
    def create_vertex_ai_tab(self):
        """Kreira tab za Vertex AI konfiguraciju"""
        ai_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(ai_frame, text="Vertex AI")
        
        # Configure grid
        ai_frame.columnconfigure(0, weight=1)
        ai_frame.rowconfigure(1, weight=1)
        
        # AI status frame
        ai_status_frame = ttk.LabelFrame(ai_frame, text="Status Vertex AI konekcije", padding="10")
        ai_status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        ai_status_frame.columnconfigure(0, weight=1)
        
        self.ai_status_text = scrolledtext.ScrolledText(ai_status_frame, height=15, width=70)
        self.ai_status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        ai_button_frame = ttk.Frame(ai_frame)
        ai_button_frame.grid(row=1, column=0, pady=(10, 0), sticky=tk.W)
        
        ttk.Button(ai_button_frame, text="Testiraj Vertex AI", 
                   command=self.test_vertex_ai_connection).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(ai_button_frame, text="Vertex AI konfiguracija", 
                   command=self.show_vertex_ai_configuration).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(ai_button_frame, text="Obriši AI config", 
                   command=self.delete_vertex_ai_configuration).pack(side=tk.LEFT)
        
        # Initial status
        self.update_ai_status("Vertex AI konfiguracija.\nKliknite 'Vertex AI konfiguracija' za setup.")
    
    def create_reports_tab(self):
        """Kreira tab za AI izveštaje"""
        reports_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(reports_frame, text="AI Izveštaji")
        
        # Configure grid
        reports_frame.columnconfigure(0, weight=1)
        reports_frame.rowconfigure(2, weight=1)
        
        # Input frame
        input_frame = ttk.LabelFrame(reports_frame, text="SQL upit za analizu", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.sql_input = scrolledtext.ScrolledText(input_frame, height=5, width=70)
        self.sql_input.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.sql_input.insert(1.0, "SELECT * FROM tickets LIMIT 10;")
        
        # Control frame
        control_frame = ttk.Frame(reports_frame)
        control_frame.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)
        
        ttk.Button(control_frame, text="Generiši izveštaj", 
                   command=self.generate_ai_report).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(control_frame, text="Tip izveštaja:").pack(side=tk.LEFT, padx=(10, 5))
        self.report_type_var = tk.StringVar(value="osnovni")
        report_combo = ttk.Combobox(control_frame, textvariable=self.report_type_var, 
                                   values=["osnovni", "detaljni", "statistički", "trend analiza"])
        report_combo.pack(side=tk.LEFT)
        
        # Output frame
        output_frame = ttk.LabelFrame(reports_frame, text="AI izveštaj", padding="10")
        output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.report_output = scrolledtext.ScrolledText(output_frame, height=15, width=70)
        self.report_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def show_database_configuration(self):
        """Prikazuje dijalog za MySQL konfiguraciju"""
        config_window = tk.Toplevel(self.root)
        config_window.title("MySQL Konfiguracija")
        config_window.geometry("450x350")
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
        fields = [
            ("IP adresa/Host:", "host", ""),
            ("Port:", "port", "3306"),
            ("Korisničko ime:", "username", ""),
            ("Lozinka:", "password", ""),
            ("Naziv baze:", "database", "")
        ]
        
        entries = {}
        for i, (label, key, default) in enumerate(fields):
            ttk.Label(config_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=(0, 5))
            var = tk.StringVar(value=existing_config.get(key, default))
            entry = ttk.Entry(config_frame, textvariable=var, width=35)
            if key == "password":
                entry.configure(show="*")
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
            entries[key] = var
        
        # Configure grid
        config_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0))
        
        def save_config():
            config_data = {key: var.get().strip() for key, var in entries.items()}
            
            # Validation
            required = ['host', 'username', 'password', 'database']
            if not all(config_data[key] for key in required):
                messagebox.showerror("Greška", "Sva polja moraju biti popunjena!")
                return
            
            if self.config_manager.save_config(config_data):
                messagebox.showinfo("Uspeh", "MySQL konfiguracija je sačuvana!")
                config_window.destroy()
                self.update_db_status("MySQL konfiguracija je ažurirana.\nKliknite 'Testiraj MySQL konekciju' za proveru.")
            else:
                messagebox.showerror("Greška", "Greška pri čuvanju konfiguracije!")
        
        ttk.Button(button_frame, text="Sačuvaj", command=save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Otkaži", command=config_window.destroy).pack(side=tk.LEFT)
    
    def show_vertex_ai_configuration(self):
        """Prikazuje dijalog za Vertex AI konfiguraciju"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Vertex AI Konfiguracija")
        config_window.geometry("500x300")
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
        existing_config = self.vertex_config_manager.load_config() or {}
        
        # Project ID
        ttk.Label(config_frame, text="Google Cloud Project ID:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        project_var = tk.StringVar(value=existing_config.get('project_id', ''))
        project_entry = ttk.Entry(config_frame, textvariable=project_var, width=40)
        project_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Region
        ttk.Label(config_frame, text="Region:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        region_var = tk.StringVar(value=existing_config.get('region', 'global'))
        region_combo = ttk.Combobox(config_frame, textvariable=region_var, width=37,
                                   values=['global', 'us-central1', 'us-east5', 'europe-west1'])
        region_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Service Account JSON path
        ttk.Label(config_frame, text="Service Account JSON:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        json_frame = ttk.Frame(config_frame)
        json_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        json_frame.columnconfigure(0, weight=1)
        
        json_path_var = tk.StringVar(value=existing_config.get('service_account_path', ''))
        json_entry = ttk.Entry(json_frame, textvariable=json_path_var, width=30)
        json_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        def browse_json():
            filename = filedialog.askopenfilename(
                title="Izaberite Service Account JSON fajl",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                json_path_var.set(filename)
        
        ttk.Button(json_frame, text="Pretraži", command=browse_json).grid(row=0, column=1)
        
        # Configure grid
        config_frame.columnconfigure(1, weight=1)
        
        # Info text
        info_text = """
Napomene:
• Project ID možete naći u Google Cloud Console
• Preporučujemo region 'global' za najbolju dostupnost modela
• Service Account JSON fajl ste preuzeli iz Google Cloud Console
"""
        info_label = ttk.Label(config_frame, text=info_text, font=("Arial", 8))
        info_label.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        def save_vertex_config():
            config_data = {
                'project_id': project_var.get().strip(),
                'region': region_var.get().strip(),
                'service_account_path': json_path_var.get().strip()
            }
            
            # Validation
            if not config_data['project_id']:
                messagebox.showerror("Greška", "Project ID je obavezan!")
                return
            
            if not config_data['service_account_path']:
                messagebox.showerror("Greška", "Service Account JSON putanja je obavezna!")
                return
            
            if self.vertex_config_manager.save_config(config_data):
                messagebox.showinfo("Uspeh", "Vertex AI konfiguracija je sačuvana!")
                config_window.destroy()
                self.update_ai_status("Vertex AI konfiguracija je ažurirana.\nKliknite 'Testiraj Vertex AI' za proveru.")
            else:
                messagebox.showerror("Greška", "Greška pri čuvanju Vertex AI konfiguracije!")
        
        ttk.Button(button_frame, text="Sačuvaj", command=save_vertex_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Otkaži", command=config_window.destroy).pack(side=tk.LEFT)
    
    def test_database_connection(self):
        """Testira MySQL konekciju"""
        config = self.config_manager.load_config()
        if not config:
            messagebox.showwarning("Upozorenje", "Prvo konfigurisajte MySQL konekciju!")
            self.show_database_configuration()
            return
        
        self.update_db_status("Testiram MySQL konekciju...\n⏳ Molimo sačekajte...")
        self.status_var.set("Testiram MySQL...")
        
        def run_test():
            connector = BLBSConnector(config)
            success, message = connector.test_connection()
            self.root.after(0, lambda: self.update_db_status(message))
            self.root.after(0, lambda: self.status_var.set("MySQL test završen"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def test_vertex_ai_connection(self):
        """Testira Vertex AI konekciju"""
        config = self.vertex_config_manager.load_config()
        if not config:
            messagebox.showwarning("Upozorenje", "Prvo konfigurisajte Vertex AI!")
            self.show_vertex_ai_configuration()
            return
        
        self.update_ai_status("Testiram Vertex AI konekciju...\n⏳ Molimo sačekajte...")
        self.status_var.set("Testiram Vertex AI...")
        
        def run_test():
            try:
                self.vertex_ai_manager = VertexAIManager(config)
                success, message = self.vertex_ai_manager.test_connection()
                self.root.after(0, lambda: self.update_ai_status(message))
                self.root.after(0, lambda: self.status_var.set("Vertex AI test završen"))
            except Exception as e:
                error_msg = f"Greška pri testiranju Vertex AI: {str(e)}"
                self.root.after(0, lambda: self.update_ai_status(error_msg))
                self.root.after(0, lambda: self.status_var.set("Vertex AI greška"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def generate_ai_report(self):
        """Generiše AI izveštaj"""
        # Proverava konfiguracije
        db_config = self.config_manager.load_config()
        ai_config = self.vertex_config_manager.load_config()
        
        if not db_config:
            messagebox.showwarning("Upozorenje", "Prvo konfigurisajte MySQL konekciju!")
            return
        
        if not ai_config:
            messagebox.showwarning("Upozorenje", "Prvo konfigurisajte Vertex AI!")
            return
        
        sql_query = self.sql_input.get(1.0, tk.END).strip()
        if not sql_query:
            messagebox.showwarning("Upozorenje", "Unesite SQL upit!")
            return
        
        self.report_output.delete(1.0, tk.END)
        self.report_output.insert(tk.END, "Generiram izveštaj...\n⏳ Molimo sačekajte...")
        self.status_var.set("Generiram AI izveštaj...")
        
        def generate_report():
            try:
                # Execute SQL query
                db_connector = BLBSConnector(db_config)
                if not db_connector.connect():
                    error_msg = "Greška: Nije moguće povezati sa MySQL bazom!"
                    self.root.after(0, lambda: self.report_output.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.report_output.insert(tk.END, error_msg))
                    return
                
                sql_results = db_connector.execute_query(sql_query)
                db_connector.disconnect()
                
                if sql_results is None:
                    error_msg = "Greška: SQL upit nije uspešno izvršen!"
                    self.root.after(0, lambda: self.report_output.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.report_output.insert(tk.END, error_msg))
                    return
                
                # Prepare data for AI
                sql_data_str = f"SQL Upit: {sql_query}\n\nRezultati:\n"
                for i, row in enumerate(sql_results[:50]):  # Limit to 50 rows
                    sql_data_str += f"Red {i+1}: {row}\n"
                
                if len(sql_results) > 50:
                    sql_data_str += f"\n... i još {len(sql_results) - 50} redova"
                
                # Generate AI report
                if not self.vertex_ai_manager:
                    self.vertex_ai_manager = VertexAIManager(ai_config)
                
                report_type = self.report_type_var.get()
                success, ai_report = self.vertex_ai_manager.generate_report(sql_data_str, report_type)
                
                if success:
                    final_report = f"=== AI IZVEŠTAJ ({report_type.upper()}) ===\n\n{ai_report}"
                else:
                    final_report = f"Greška pri generisanju AI izveštaja: {ai_report}"
                
                self.root.after(0, lambda: self.report_output.delete(1.0, tk.END))
                self.root.after(0, lambda: self.report_output.insert(tk.END, final_report))
                self.root.after(0, lambda: self.status_var.set("AI izveštaj generisan"))
                
            except Exception as e:
                error_msg = f"Greška: {str(e)}"
                self.root.after(0, lambda: self.report_output.delete(1.0, tk.END))
                self.root.after(0, lambda: self.report_output.insert(tk.END, error_msg))
                self.root.after(0, lambda: self.status_var.set("Greška pri generisanju"))
        
        threading.Thread(target=generate_report, daemon=True).start()
    
    def delete_database_configuration(self):
        """Briše MySQL konfiguraciju"""
        if messagebox.askyesno("Potvrda", "Da li ste sigurni da želite da obrišete MySQL konfiguraciju?"):
            if self.config_manager.delete_config():
                messagebox.showinfo("Uspeh", "MySQL konfiguracija je obrisana!")
                self.update_db_status("MySQL konfiguracija je obrisana.\nPotrebno je ponovo konfigurisati konekciju.")
            else:
                messagebox.showerror("Greška", "Greška pri brisanju MySQL konfiguracije!")
    
    def delete_vertex_ai_configuration(self):
        """Briše Vertex AI konfiguraciju"""
        if messagebox.askyesno("Potvrda", "Da li ste sigurni da želite da obrišete Vertex AI konfiguraciju?"):
            if self.vertex_config_manager.delete_config():
                messagebox.showinfo("Uspeh", "Vertex AI konfiguracija je obrisana!")
                self.update_ai_status("Vertex AI konfiguracija je obrisana.\nPotrebno je ponovo konfigurisati konekciju.")
                self.vertex_ai_manager = None
            else:
                messagebox.showerror("Greška", "Greška pri brisanju Vertex AI konfiguracije!")
    
    def update_db_status(self, message: str):
        """Ažurira MySQL status tekst"""
        self.db_status_text.delete(1.0, tk.END)
        self.db_status_text.insert(1.0, message)
        self.db_status_text.see(tk.END)
    
    def update_ai_status(self, message: str):
        """Ažurira Vertex AI status tekst"""
        self.ai_status_text.delete(1.0, tk.END)
        self.ai_status_text.insert(1.0, message)
        self.ai_status_text.see(tk.END)
    
    def check_initial_setup(self):
        """Proverava početni setup"""
        if not self.config_manager.is_configured():
            self.update_db_status("MySQL nije konfigurisan.\nKliknite 'MySQL konfiguracija' za setup.")
        else:
            self.update_db_status("MySQL konfiguracija pronađena.\nKliknite 'Testiraj MySQL konekciju' za proveru.")
        
        if not self.vertex_config_manager.is_configured():
            self.update_ai_status("Vertex AI nije konfigurisan.\nKliknite 'Vertex AI konfiguracija' za setup.")
        else:
            self.update_ai_status("Vertex AI konfiguracija pronađena.\nKliknite 'Testiraj Vertex AI' za proveru.")
    
    def run(self):
        """Pokretanje aplikacije"""
        self.root.mainloop()