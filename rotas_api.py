from flask import Blueprint, jsonify
from estado_global import status_salas

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