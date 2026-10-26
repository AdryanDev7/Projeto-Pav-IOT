from controllers.base_controller import BaseController


class OperadorController(BaseController):
    def listar_para_login(self):
        return self._service.listar_para_login()
