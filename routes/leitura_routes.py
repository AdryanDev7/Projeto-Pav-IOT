from flask import Blueprint
from controllers.leitura_controller import LeituraController

leitura_bp = Blueprint('leitura_bp', __name__, url_prefix='/api/leituras')

leitura_bp.route('', methods=['POST'])(LeituraController.criar_leitura)
leitura_bp.route('', methods=['GET'])(LeituraController.listar_leituras)
leitura_bp.route('/<int:leitura_id>', methods=['DELETE'])(LeituraController.deletar_leitura)