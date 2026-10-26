from config.excecoes import ConflitoErro
from config.settings import agora
from services.dependente_sensor_service import DependenteSensorService


class AlertaService(DependenteSensorService):
    nome_entidade = "Alerta"

    def _aplicar(self, obj, dados, operador):
        super()._aplicar(obj, dados, operador)
        if obj.status == "RECONHECIDO" and obj.reconhecido_por is None:
            obj.reconhecido_por = operador.id
            obj.reconhecido_em = agora()

    def reconhecer(self, id_, operador):
        """Operador confirma o alerta no painel (evita o escalonamento da regra 9)."""
        alerta = self._obter(id_)
        self._autorizar(operador, alerta, escrita=True)
        if alerta.status == "RECONHECIDO":
            raise ConflitoErro("Este alerta já foi reconhecido.")
        alerta.status = "RECONHECIDO"
        alerta.reconhecido_por = operador.id
        alerta.reconhecido_em = agora()
        return self._repo.salvar(alerta)
