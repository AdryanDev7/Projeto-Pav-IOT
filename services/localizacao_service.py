from repositories.localizacao_repository import LocalizacaoRepository
from entities.localizacao import Localizacao

class LocalizacaoService:
    @staticmethod
    def listar_localizacoes():
        localizacoes = LocalizacaoRepository.listar_todos()
        return [
            {
                "id": l.id,
                "nome": l.nome,
                "setor": l.setor,
                "latitude": float(l.latitude),
                "longitude": float(l.longitude)
            } for l in localizacoes
        ]

    @staticmethod
    def criar_localizacao(dados):
        nova_loc = Localizacao(
            nome=dados.get("nome"),
            setor=dados.get("setor"),
            latitude=dados.get("latitude"),
            longitude=dados.get("longitude")
        )
        LocalizacaoRepository.salvar(nova_loc)
        return nova_loc

    @staticmethod
    def atualizar_localizacao(id, dados):
        loc = LocalizacaoRepository.buscar_por_id(id)
        if not loc:
            return None
        loc.nome = dados.get("nome", loc.nome)
        loc.setor = dados.get("setor", loc.setor)
        loc.latitude = dados.get("latitude", loc.latitude)
        loc.longitude = dados.get("longitude", loc.longitude)
        LocalizacaoRepository.salvar(loc)
        return loc

    @staticmethod
    def deletar_localizacao(id):
        loc = LocalizacaoRepository.buscar_por_id(id)
        if not loc:
            return False
        LocalizacaoRepository.excluir(loc)
        return True