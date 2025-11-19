import subprocess
import hashlib
from flask import Flask, request 

app = Flask(__name__)

# --- Nível 3: Taint Analysis (Fluxo de Dados) ---
# O SonarQube deve apanhar isto.
# O Bandit pode apanhar o shell=True, mas não o fluxo.
@app.route("/run") 
def run_command():
    # FONTE (Taint): Input do utilizador
    command = request.args.get('cmd') 
    
    # POÇO (Sink): Execucao de shell com dados "manchados"
    subprocess.call(command, shell=True) 
    return "Command executed"

# --- Nível 2: Padrão Semântico (Conteúdo) ---
# O Semgrep deve apanhar isto. O Bandit vai falhar.
def get_api_key(): 
    # Risco: Chave de API no codigo
    API_KEY = "sk_live_123456789abcdefgHJKL" 
    return API_KEY

# --- Nível 1: Padrão AST (Estrutura) ---
# O Bandit deve apanhar isto.
def hash_password(password):  
    # Risco: Uso de MD5 para passwords
    return hashlib.md5(password.encode()).hexdigest()  # 

# --- Nível 1: Padrão AST (Estrutura) ---
# O Bandit deve apanhar isto.
def check_admin(is_admin): 
    # Risco: 'assert' e removido com otimizacao
    assert is_admin, "User is not admin"  
    return True
