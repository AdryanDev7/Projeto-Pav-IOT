"""Funções de autorização (regra 10: isolamento por zona)."""
from config.excecoes import AcessoNegadoErro


def zona_do_operador(operador):
    """Retorna a zona que restringe a visão do operador, ou None se vê tudo (supervisor)."""
    return operador.zona if operador.perfil == "OPERADOR" else None


def exigir_zona(operador, zona_do_recurso: str) -> None:
    """Operador comum só mexe em recursos da própria zona. Supervisor mexe em tudo."""
    if operador.perfil == "OPERADOR" and operador.zona != zona_do_recurso:
        raise AcessoNegadoErro(
            f"Acesso negado: o recurso pertence à zona '{zona_do_recurso}' "
            f"e você está cadastrado na zona '{operador.zona}'.")


def exigir_supervisor(operador) -> None:
    if operador.perfil != "SUPERVISOR":
        raise AcessoNegadoErro("Apenas supervisores podem executar esta operação.")
