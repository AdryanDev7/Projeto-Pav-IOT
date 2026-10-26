from controllers.base_controller import BaseController


class AlertaController(BaseController):
    def reconhecer(self, id_, operador):
        return self._service.reconhecer(id_, operador)
