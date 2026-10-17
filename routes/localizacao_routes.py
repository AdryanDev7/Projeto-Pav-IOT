from flask import Blueprint
from controllers.localizacao_controller import LocalizacaoController

localizacao_bp = Blueprint('localizacao_bp', __name__, url_prefix='/api/localizacoes')

localizacao_bp.route('', methods=['POST'])(LocalizacaoController.criar_localizacao)
localizacao_bp.route('', methods=['GET'])(LocalizacaoController.listar_localizacoes)
localizacao_bp.route('/<int:localizacao_id>', methods=['PUT'])(LocalizacaoController.atualizar_localizacao)
localizacao_bp.route('/<int:localizacao_id>', methods=['DELETE'])(LocalizacaoController.deletar_localizacao)