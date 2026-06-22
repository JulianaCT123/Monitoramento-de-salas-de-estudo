from flask import Flask
from flask_cors import CORS
from rotas_api import api_blueprint
import threading
from comunicacao_serial import iniciar_leitura_arduino

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Ativa o CORS para evitar bloqueios caso alguém acesse a API de outro IP/Porta
CORS(app)

# Registra as rotas (a página HTML e os endpoints /api/salas) que estão no outro arquivo
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    # ==========================================
    # 1. INICIALIZAÇÃO DO HARDWARE (Em Background)
    # ==========================================
    print("[SISTEMA] Iniciando a Thread de leitura do Arduino...")
    thread_arduino = threading.Thread(target=iniciar_leitura_arduino, daemon=True)
    thread_arduino.start()
    
    print("[SISTEMA] Iniciando o servidor web Flask...")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)