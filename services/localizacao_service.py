from repositories.localizacao_repository import LocalizacaoRepository
from entities.models import Localizacao

class LocalizacaoService:
    @staticmethod
    def criar_localizacao(dados):
        # Validação simples de campos obrigatórios
        if not dados.get('nome') or not dados.get('setor'):
            raise ValueError("Nome e setor da localização são obrigatórios.")

        nova_localizacao = Localizacao(
            nome=dados.get('nome'),
            setor=dados.get('setor'),
            latitude=dados.get('latitude', 0.0),
            longitude=dados.get('longitude', 0.0)
        )
        return LocalizacaoRepository.salvar(nova_localizacao)

    @staticmethod
    def listar_localizacoes():
        locs = LocalizacaoRepository.listar_todas()
        return [
            {
                "id": l.id,
                "nome": l.nome,
                "setor": l.setor,
                "latitude": float(l.latitude),
                "longitude": float(l.longitude)
            } for l in locs
        ]

    @staticmethod
    def atualizar_localizacao(localizacao_id, dados):
        localizacao = LocalizacaoRepository.buscar_por_id(localizacao_id)
        if not localizacao:
            raise ValueError("Localização não encontrada.")

        localizacao.nome = dados.get('nome', localizacao.nome)
        localizacao.setor = dados.get('setor', localizacao.setor)
        localizacao.latitude = dados.get('latitude', localizacao.latitude)
        localizacao.longitude = dados.get('longitude', localizacao.longitude)

        LocalizacaoRepository.atualizar()
        return localizacao

    @staticmethod
    def deletar_localizacao(localizacao_id):
        localizacao = LocalizacaoRepository.buscar_por_id(localizacao_id)
        if not localizacao:
            raise ValueError("Localização não encontrada.")
        
        LocalizacaoRepository.deletar(localizacao)
        return True