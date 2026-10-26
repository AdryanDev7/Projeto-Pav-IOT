"""Controller genérico: só repassa para o service. Controllers NÃO têm regra de negócio."""


class BaseController:
    def __init__(self, service):
        self._service = service

    def listar(self, operador):
        return self._service.listar(operador)

    def buscar(self, id_, operador):
        return self._service.buscar(id_, operador)

    def criar(self, dados, operador):
        return self._service.criar(dados, operador)

    def atualizar(self, id_, dados, operador):
        return self._service.atualizar(id_, dados, operador)

    def remover(self, id_, operador):
        self._service.remover(id_, operador)
