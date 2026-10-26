"""Exceções de negócio. Cada uma carrega o código HTTP correspondente.
O app.py registra um handler que converte qualquer ErroNegocio em resposta JSON,
então services e controllers não precisam conhecer detalhes do FastAPI."""


class ErroNegocio(Exception):
    status_code = 400

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class NaoAutenticadoErro(ErroNegocio):
    status_code = 401


class AcessoNegadoErro(ErroNegocio):
    status_code = 403


class NaoEncontradoErro(ErroNegocio):
    status_code = 404


class OperacaoNaoPermitidaErro(ErroNegocio):
    status_code = 405


class ConflitoErro(ErroNegocio):
    status_code = 409


class RegraVioladaErro(ErroNegocio):
    status_code = 422
