from repositories.anomalia_repository import AnomaliaRepository
from entities.anomalia import Anomalia

class AnomaliaService:
    @staticmethod
    def listar_anomalias():
        anomalias = AnomaliaRepository.listar_todos()
        return [
            {
                "id": a.id,
                "leitura_id": a.leitura_id,
                "descricao_alerta": a.descricao_alerta,
                "severidade": a.severidade
            } for a in anomalias
        ]

    @staticmethod
    def criar_anomalia(dados):
        nova_anomalia = Anomalia(
            leitura_id=dados.get("leitura_id"),
            descricao_alerta=dados.get("descricao_alerta"),
            severidade=dados.get("severidade")
        )
        AnomaliaRepository.salvar(nova_anomalia)
        return nova_anomalia

    @staticmethod
    def deletar_anomalia(id):
        anomalia = AnomaliaRepository.buscar_por_id(id)
        if not anomalia:
            return False
        AnomaliaRepository.excluir(anomalia)
        return True