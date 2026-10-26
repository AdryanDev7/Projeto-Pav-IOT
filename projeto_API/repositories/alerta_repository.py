from entities.models import Alerta, Sensor
from repositories.base_repository import BaseRepository


class AlertaRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Alerta)

    def listar_filtrado(self, zona=None):
        consulta = self._db.query(Alerta)
        if zona:
            consulta = consulta.join(Sensor, Sensor.id == Alerta.sensor_id).filter(Sensor.zona == zona)
        return consulta.order_by(Alerta.criado_em.desc()).all()

    def altos_sem_reconhecimento_antes_de(self, corte):
        """Alertas ALTA ainda ABERTOS criados antes do 'corte' (regra 9)."""
        return (self._db.query(Alerta)
                .filter(Alerta.status == "ABERTO", Alerta.prioridade == "ALTA",
                        Alerta.criado_em < corte)
                .all())
