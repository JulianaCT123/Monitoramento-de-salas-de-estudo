from flask import Blueprint, jsonify
from estado_global import status_salas, historico_eventos
from datetime import datetime

api_blueprint = Blueprint('api', __name__)

# Rota para listar TODAS as salas de uma vez
@api_blueprint.route('/api/salas', methods=['GET'])
def listar_todas_salas():
    # Retorna o dicionário completo
    return jsonify(status_salas)

# Rota dinâmica para buscar uma sala específica pelo ID
@api_blueprint.route('/api/salas/<id_sala>', methods=['GET'])
def obter_status_sala(id_sala):
    if id_sala in status_salas:
        return jsonify(status_salas[id_sala])
    else:
        # Retorna erro 404 se tentarem buscar uma sala que não existe
        return jsonify({"erro": "Sala não encontrada"}), 404
    
# NOVA ROTA - Ocupar sala
@api_blueprint.route('/api/ocupar/<id_sala>', methods=['POST'])
def ocupar_sala(id_sala):

    if id_sala in status_salas:
        status_salas[id_sala]["ocupada"] = True

        status_salas[id_sala]["tempo_ocupacao"] = datetime.now().isoformat()

        historico_eventos.insert(0,
        f"{datetime.now().strftime('%H:%M:%S')} - Sala {id_sala} ocupada"
        )

        del historico_eventos[10:]

        import threading 
        import time

        def ligar_luz(): 
            time.sleep(1) 
            status_salas[id_sala]["luz"] = True

            historico_eventos.insert(0,
            f"{datetime.now().strftime('%H:%M:%S')} - Luz da sala {id_sala} ligada"
            )

            del historico_eventos[10:]

        threading.Thread( 
            target=ligar_luz, 
            daemon=True 
        ).start()

        return jsonify({
            "mensagem": f"Sala {id_sala} ocupada com sucesso"
        })

    return jsonify({
        "erro": "Sala não encontrada"
    }), 404


# NOVA ROTA - Liberar sala
@api_blueprint.route('/api/liberar/<id_sala>', methods=['POST'])
def liberar_sala(id_sala):

    if id_sala in status_salas:
        status_salas[id_sala]["ocupada"] = False
        status_salas[id_sala]["tempo_ocupacao"] = None
        
        historico_eventos.insert(0,
        f"{datetime.now().strftime('%H:%M:%S')} - Sala {id_sala} liberada"
        )
        
        del historico_eventos[10:]
        
        import threading 
        import time

        def desligar_luz(): 
            time.sleep(1) 
            status_salas[id_sala]["luz"] = False

            historico_eventos.insert(0,
            f"{datetime.now().strftime('%H:%M:%S')} - Luz da sala {id_sala} desligada"
            )

            del historico_eventos[10:]

        threading.Thread( 
            target=desligar_luz, 
            daemon=True 
        ).start()

        return jsonify({
            "mensagem": f"Sala {id_sala} liberada com sucesso"
        })

    return jsonify({
        "erro": "Sala não encontrada"
    }), 404

@api_blueprint.route('/api/historico', methods=['GET'])
def obter_historico():

    return jsonify(historico_eventos)