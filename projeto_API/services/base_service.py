"""Service genérico com o fluxo padrão de CRUD. As subclasses só sobrescrevem os
'ganchos' (métodos que começam com _) para colocar suas regras de negócio.
Isso é o padrão Template Method: o esqueleto fica aqui, os detalhes nas filhas."""
from config.excecoes import NaoEncontradoErro
from services.autorizacao import zona_do_operador


class BaseService:
    nome_entidade = "Registro"

    def __init__(self, repo):
        self._repo = repo

    # ---------------------------------------------------- operações públicas
    def listar(self, operador):
        return self._repo.listar_filtrado(zona_do_operador(operador))

    def buscar(self, id_, operador):
        obj = self._obter(id_)
        self._autorizar(operador, obj, escrita=False)
        return obj

    def criar(self, dados, operador):
        self._validar(dados, operador)
        obj = self._montar(dados)
        self._autorizar(operador, obj, escrita=True)
        self._ajustar(obj)
        return self._repo.salvar(obj)

    def atualizar(self, id_, dados, operador):
        obj = self._obter(id_)
        self._autorizar(operador, obj, escrita=True)
        self._validar(dados, operador)
        self._aplicar(obj, dados, operador)
        self._ajustar(obj)
        return self._repo.salvar(obj)

    def remover(self, id_, operador):
        obj = self._obter(id_)
        self._autorizar(operador, obj, escrita=True)
        self._antes_de_remover(obj, operador)
        self._repo.remover(obj)

    # ------------------------------------------- ganchos (sobrescreva nas filhas)
    def _obter(self, id_):
        obj = self._repo.buscar(id_)
        if obj is None:
            raise NaoEncontradoErro(f"{self.nome_entidade} {id_} não encontrado(a).")
        return obj

    def _autorizar(self, operador, obj, escrita: bool) -> None:
        """Por padrão qualquer operador autenticado pode tudo."""

    def _validar(self, dados, operador) -> None:
        """Regras de negócio sobre os dados recebidos."""

    def _montar(self, dados):
        return self._repo.modelo(**dados.model_dump(exclude_none=True))

    def _aplicar(self, obj, dados, operador) -> None:
        for campo, valor in dados.model_dump(exclude_none=True).items():
            setattr(obj, campo, valor)

    def _ajustar(self, obj) -> None:
        """Últimos acertos no objeto antes de gravar."""

    def _antes_de_remover(self, obj, operador) -> None:
        """Regras que podem impedir a exclusão."""
