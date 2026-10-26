class LeituraController:
    def __init__(self, service):
        self._service = service

    def registrar(self, dados):
        return self._service.registrar(dados)

    def listar(self, operador, sensor_id=None, limite=100):
        return self._service.listar(operador, sensor_id, limite)

    def buscar(self, id_, operador):
        return self._service.buscar(id_, operador)

    def bloquear_alteracao(self):
        self._service.bloquear_alteracao()
