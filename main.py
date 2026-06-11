import threading
from flask import Flask
from flask_cors import CORS

# Importamos os módulos que criamos
from rotas_api import api_blueprint
from comunicacao_serial import iniciar_leitura_arduino

app = Flask(__name__)
CORS(app)

# Registramos as rotas separadas no aplicativo principal
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    # 1. Dá a partida na thread do Arduino
    thread_hardware = threading.Thread(target=iniciar_leitura_arduino, daemon=True)
    thread_hardware.start()
    
    # 2. Dá a partida no servidor web
    print("Servidor rodando! Pressione CTRL+C para sair.")
    app.run(host='0.0.0.0', port=5000, debug=False)