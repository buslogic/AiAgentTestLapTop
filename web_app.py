"""
BLBS AI Agent - Web verzija
"""
import sys
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import threading

# Dodaj project root u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config_manager import ConfigManager
from config.vertex_config_manager import VertexConfigManager
from database.blbs_connector import BLBSConnector
from ai.vertex_ai_manager import VertexAIManager

app = Flask(__name__)

# Global managers
config_manager = ConfigManager()
vertex_config_manager = VertexConfigManager()
vertex_ai_manager = None

@app.route('/')
def index():
    """Glavna stranica"""
    mysql_configured = config_manager.is_configured()
    vertex_configured = vertex_config_manager.is_configured()
    
    return render_template('index.html', 
                         mysql_configured=mysql_configured,
                         vertex_configured=vertex_configured)

@app.route('/mysql')
def mysql_page():
    """MySQL konfiguracija stranica"""
    config = config_manager.load_config() or {}
    return render_template('mysql.html', config=config)

@app.route('/mysql/save', methods=['POST'])
def save_mysql():
    """Čuva MySQL konfiguraciju"""
    data = request.json
    
    # Validation
    required = ['host', 'username', 'password', 'database']
    if not all(data.get(key) for key in required):
        return jsonify({'success': False, 'message': 'Sva polja moraju biti popunjena!'})
    
    if config_manager.save_config(data):
        return jsonify({'success': True, 'message': 'MySQL konfiguracija je sačuvana!'})
    else:
        return jsonify({'success': False, 'message': 'Greška pri čuvanju konfiguracije!'})

@app.route('/mysql/test', methods=['POST'])
def test_mysql():
    """Testira MySQL konekciju"""
    config = config_manager.load_config()
    if not config:
        return jsonify({'success': False, 'message': 'Prvo konfigurisajte MySQL konekciju!'})
    
    try:
        connector = BLBSConnector(config)
        success, message = connector.test_connection()
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Greška: {str(e)}'})

@app.route('/vertex')
def vertex_page():
    """Vertex AI konfiguracija stranica"""
    config = vertex_config_manager.load_config() or {}
    return render_template('vertex.html', config=config)

@app.route('/vertex/save', methods=['POST'])
def save_vertex():
    """Čuva Vertex AI konfiguraciju"""
    data = request.json
    
    # Validation
    if not data.get('project_id'):
        return jsonify({'success': False, 'message': 'Project ID je obavezan!'})
    
    if not data.get('service_account_path'):
        return jsonify({'success': False, 'message': 'Service Account JSON putanja je obavezna!'})
    
    if vertex_config_manager.save_config(data):
        return jsonify({'success': True, 'message': 'Vertex AI konfiguracija je sačuvana!'})
    else:
        return jsonify({'success': False, 'message': 'Greška pri čuvanju Vertex AI konfiguracije!'})

@app.route('/vertex/test', methods=['POST'])
def test_vertex():
    """Testira Vertex AI konekciju"""
    global vertex_ai_manager
    
    config = vertex_config_manager.load_config()
    if not config:
        return jsonify({'success': False, 'message': 'Prvo konfigurisajte Vertex AI!'})
    
    try:
        vertex_ai_manager = VertexAIManager(config)
        success, message = vertex_ai_manager.test_connection()
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Greška pri testiranju Vertex AI: {str(e)}'})

@app.route('/reports')
def reports_page():
    """AI izveštaji stranica"""
    return render_template('reports.html')

@app.route('/reports/generate', methods=['POST'])
def generate_report():
    """Generiše AI izveštaj"""
    global vertex_ai_manager
    
    data = request.json
    sql_query = data.get('sql_query', '').strip()
    report_type = data.get('report_type', 'osnovni')
    
    if not sql_query:
        return jsonify({'success': False, 'message': 'Unesite SQL upit!'})
    
    # Proverava konfiguracije
    db_config = config_manager.load_config()
    ai_config = vertex_config_manager.load_config()
    
    if not db_config:
        return jsonify({'success': False, 'message': 'Prvo konfigurisajte MySQL konekciju!'})
    
    if not ai_config:
        return jsonify({'success': False, 'message': 'Prvo konfigurisajte Vertex AI!'})
    
    try:
        # Execute SQL query
        db_connector = BLBSConnector(db_config)
        if not db_connector.connect():
            return jsonify({'success': False, 'message': 'Greška: Nije moguće povezati sa MySQL bazom!'})
        
        sql_results = db_connector.execute_query(sql_query)
        db_connector.disconnect()
        
        if sql_results is None:
            return jsonify({'success': False, 'message': 'Greška: SQL upit nije uspešno izvršen!'})
        
        # Prepare data for AI
        sql_data_str = f"SQL Upit: {sql_query}\\n\\nRezultati:\\n"
        for i, row in enumerate(sql_results[:50]):  # Limit to 50 rows
            sql_data_str += f"Red {i+1}: {row}\\n"
        
        if len(sql_results) > 50:
            sql_data_str += f"\\n... i još {len(sql_results) - 50} redova"
        
        # Generate AI report
        if not vertex_ai_manager:
            vertex_ai_manager = VertexAIManager(ai_config)
        
        success, ai_report = vertex_ai_manager.generate_report(sql_data_str, report_type)
        
        if success:
            final_report = f"=== AI IZVEŠTAJ ({report_type.upper()}) ===\\n\\n{ai_report}"
            return jsonify({'success': True, 'report': final_report})
        else:
            return jsonify({'success': False, 'message': f'Greška pri generisanju AI izveštaja: {ai_report}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Greška: {str(e)}'})

# Create templates directory
import os
if not os.path.exists('templates'):
    os.makedirs('templates')

# HTML templates
INDEX_HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>BLBS AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
        .nav { display: flex; gap: 10px; margin-bottom: 20px; }
        .nav a { padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        .nav a:hover { background: #2980b9; }
        .status { padding: 15px; margin: 10px 0; border-radius: 4px; }
        .status.ok { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🚀 BLBS AI Agent - Web Verzija</h1>
        
        <div class="nav">
            <a href="/mysql">MySQL Konfiguracija</a>
            <a href="/vertex">Vertex AI Konfiguracija</a>
            <a href="/reports">AI Izveštaji</a>
        </div>
        
        <h2>Status Konfiguracije</h2>
        
        <div class="status {% if mysql_configured %}ok{% else %}error{% endif %}">
            <strong>MySQL:</strong> 
            {% if mysql_configured %}
                ✅ Konfigurisan
            {% else %}
                ❌ Nije konfigurisan
            {% endif %}
        </div>
        
        <div class="status {% if vertex_configured %}ok{% else %}error{% endif %}">
            <strong>Vertex AI:</strong> 
            {% if vertex_configured %}
                ✅ Konfigurisan  
            {% else %}
                ❌ Nije konfigurisan
            {% endif %}
        </div>
        
        {% if mysql_configured and vertex_configured %}
        <div class="status ok">
            <strong>🎉 Sve je konfigurisano!</strong> Možete koristiti AI izveštaje.
        </div>
        {% endif %}
    </div>
</body>
</html>'''

MYSQL_HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>MySQL Konfiguracija - BLBS AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { padding: 10px 20px; margin: 5px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .back { background: #95a5a6; }
        .back:hover { background: #7f8c8d; }
        .test { background: #e74c3c; }
        .test:hover { background: #c0392b; }
        .message { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .status { background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ MySQL Konfiguracija</h1>
        
        <form id="mysqlForm">
            <div class="form-group">
                <label for="host">IP adresa/Host:</label>
                <input type="text" id="host" name="host" value="{{ config.host or '' }}" required>
            </div>
            
            <div class="form-group">
                <label for="port">Port:</label>
                <input type="text" id="port" name="port" value="{{ config.port or '3306' }}" required>
            </div>
            
            <div class="form-group">
                <label for="username">Korisničko ime:</label>
                <input type="text" id="username" name="username" value="{{ config.username or '' }}" required>
            </div>
            
            <div class="form-group">
                <label for="password">Lozinka:</label>
                <input type="password" id="password" name="password" value="{{ config.password or '' }}" required>
            </div>
            
            <div class="form-group">
                <label for="database">Naziv baze:</label>
                <input type="text" id="database" name="database" value="{{ config.database or '' }}" required>
            </div>
            
            <button type="submit">Sačuvaj Konfiguraciju</button>
            <button type="button" class="test" onclick="testConnection()">Testiraj Konekciju</button>
            <button type="button" class="back" onclick="location.href='/'">Nazad</button>
        </form>
        
        <div id="message"></div>
        <div id="status" class="status" style="display: none;"></div>
    </div>

    <script>
        document.getElementById('mysqlForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            fetch('/mysql/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                const messageDiv = document.getElementById('message');
                messageDiv.className = 'message ' + (result.success ? 'success' : 'error');
                messageDiv.textContent = result.message;
            });
        });
        
        function testConnection() {
            const statusDiv = document.getElementById('status');
            statusDiv.style.display = 'block';
            statusDiv.textContent = 'Testiram konekciju...⏳';
            
            fetch('/mysql/test', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(result => {
                statusDiv.textContent = result.message;
            });
        }
    </script>
</body>
</html>'''

VERTEX_HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>Vertex AI Konfiguracija - BLBS AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { padding: 10px 20px; margin: 5px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .back { background: #95a5a6; }
        .back:hover { background: #7f8c8d; }
        .test { background: #e74c3c; }
        .test:hover { background: #c0392b; }
        .message { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .status { background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
        .info { background: #e7f3ff; padding: 10px; margin: 10px 0; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Vertex AI Konfiguracija</h1>
        
        <form id="vertexForm">
            <div class="form-group">
                <label for="project_id">Google Cloud Project ID:</label>
                <input type="text" id="project_id" name="project_id" value="{{ config.project_id or '' }}" required>
            </div>
            
            <div class="form-group">
                <label for="region">Region:</label>
                <select id="region" name="region">
                    <option value="europe-west1" {% if config.region == 'europe-west1' or not config.region %}selected{% endif %}>europe-west1</option>
                    <option value="global" {% if config.region == 'global' %}selected{% endif %}>global</option>
                    <option value="us-central1" {% if config.region == 'us-central1' %}selected{% endif %}>us-central1</option>
                    <option value="us-east5" {% if config.region == 'us-east5' %}selected{% endif %}>us-east5</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="service_account_path">Service Account JSON putanja:</label>
                <input type="text" id="service_account_path" name="service_account_path" 
                       value="{{ config.service_account_path or '' }}" required
                       placeholder="C:\\path\\to\\service-account.json">
            </div>
            
            <div class="info">
                <strong>Napomene:</strong><br>
                • Project ID možete naći u Google Cloud Console<br>
                • Preporučujemo region 'europe-west1' gde ste aktivirali Claude Sonnet 4<br>
                • Service Account JSON fajl ste preuzeli iz Google Cloud Console
            </div>
            
            <button type="submit">Sačuvaj Konfiguraciju</button>
            <button type="button" class="test" onclick="testConnection()">Testiraj Vertex AI</button>
            <button type="button" class="back" onclick="location.href='/'">Nazad</button>
        </form>
        
        <div id="message"></div>
        <div id="status" class="status" style="display: none;"></div>
    </div>

    <script>
        document.getElementById('vertexForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            fetch('/vertex/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                const messageDiv = document.getElementById('message');
                messageDiv.className = 'message ' + (result.success ? 'success' : 'error');
                messageDiv.textContent = result.message;
            });
        });
        
        function testConnection() {
            const statusDiv = document.getElementById('status');
            statusDiv.style.display = 'block';
            statusDiv.textContent = 'Testiram Vertex AI konekciju...⏳ Molimo sačekajte...';
            
            fetch('/vertex/test', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(result => {
                statusDiv.textContent = result.message;
            });
        }
    </script>
</body>
</html>'''

REPORTS_HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>AI Izveštaji - BLBS AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        textarea, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { padding: 10px 20px; margin: 5px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .back { background: #95a5a6; }
        .back:hover { background: #7f8c8d; }
        .message { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .report { background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 4px; white-space: pre-wrap; font-family: monospace; min-height: 200px; }
        .controls { display: flex; gap: 10px; align-items: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 AI Izveštaji</h1>
        
        <div class="form-group">
            <label for="sqlQuery">SQL upit za analizu:</label>
            <textarea id="sqlQuery" rows="5" placeholder="SELECT * FROM tickets LIMIT 10;">SELECT * FROM tickets LIMIT 10;</textarea>
        </div>
        
        <div class="controls">
            <label for="reportType">Tip izveštaja:</label>
            <select id="reportType">
                <option value="osnovni">Osnovni</option>
                <option value="detaljni">Detaljni</option>
                <option value="statistički">Statistički</option>
                <option value="trend analiza">Trend analiza</option>
            </select>
            
            <button onclick="generateReport()">Generiši Izveštaj</button>
            <button class="back" onclick="location.href='/'">Nazad</button>
        </div>
        
        <div id="message"></div>
        
        <div class="form-group">
            <label>AI Izveštaj:</label>
            <div id="report" class="report">Ovde će se prikazati AI izveštaj...</div>
        </div>
    </div>

    <script>
        function generateReport() {
            const sqlQuery = document.getElementById('sqlQuery').value.trim();
            const reportType = document.getElementById('reportType').value;
            const reportDiv = document.getElementById('report');
            const messageDiv = document.getElementById('message');
            
            if (!sqlQuery) {
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Unesite SQL upit!';
                return;
            }
            
            reportDiv.textContent = 'Generiram izveštaj...⏳ Molimo sačekajte...';
            messageDiv.textContent = '';
            
            fetch('/reports/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    sql_query: sqlQuery,
                    report_type: reportType
                })
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    reportDiv.textContent = result.report;
                    messageDiv.className = 'message success';
                    messageDiv.textContent = 'Izveštaj je uspešno generisan!';
                } else {
                    reportDiv.textContent = 'Greška pri generisanju izveštaja.';
                    messageDiv.className = 'message error';
                    messageDiv.textContent = result.message;
                }
            })
            .catch(error => {
                reportDiv.textContent = 'Greška pri komunikaciji sa serverom.';
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Greška: ' + error.message;
            });
        }
    </script>
</body>
</html>'''

# Write templates
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(INDEX_HTML)
with open('templates/mysql.html', 'w', encoding='utf-8') as f:
    f.write(MYSQL_HTML)
with open('templates/vertex.html', 'w', encoding='utf-8') as f:
    f.write(VERTEX_HTML)
with open('templates/reports.html', 'w', encoding='utf-8') as f:
    f.write(REPORTS_HTML)

if __name__ == '__main__':
    print("*** Pokretam BLBS AI Agent Web verziju ***")
    print("Otvori browser na: http://localhost:5000")
    print("Za zaustavljanje pritisni Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=5000)