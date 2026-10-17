from repositories.anomalia_repository import AnomaliaRepository

class AnomaliaService:
    @staticmethod
    def listar_anomalias():
        anomalias = AnomaliaRepository.listar_todas()
        return [
            {
                "id": a.id,
                "leitura_id": a.leitura_id,
                "descricao_alerta": a.descricao_alerta,
                "severidade": a.severidade
            } for a in anomalias
        ]

    @staticmethod
    def deletar_anomalia(anomalia_id):
        anomalia = AnomaliaRepository.buscar_por_id(anomalia_id)
        if not anomalia:
            raise ValueError("Anomalia não encontrada.")
        AnomaliaRepository.deletar(anomalia)
        return True