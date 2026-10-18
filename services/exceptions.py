class NaoEncontradoError(Exception):
    """O registro pedido não existe (vira HTTP 404)."""


class RegraNegocioError(Exception):
    """Dado inválido ou violação de regra de negócio (vira HTTP 400)."""
