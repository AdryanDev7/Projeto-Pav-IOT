from sqlalchemy.exc import IntegrityError

from services.exceptions import NaoEncontradoError, RegraNegocioError


class BaseService:
    """
    Serviço genérico (HERANÇA). Implementa o CRUD uma vez só; as filhas
    sobrescrevem os "ganchos" (_validar, _montar, _antes_de_excluir...) com as
    regras de negócio de cada entidade (POLIMORFISMO).
    """

    _ENTIDADE = None  # classe do modelo, definida pelas filhas
    _MSG_NAO_ENCONTRADO = "Registro não encontrado."
    _MSG_INTEGRIDADE = "A operação viola a integridade dos dados."
    _MSG_EXCLUSAO_BLOQUEADA = "Não é possível excluir este registro pois existem dados associados."

    def __init__(self, repositorio):
        # CONSTRUTOR + ENCAPSULAMENTO: dependência guardada em atributo privado
        self._repo = repositorio

    # ---------- operações públicas (usadas pelos controllers) ----------
    def listar(self):
        return [entidade.to_dict() for entidade in self._repo.listar_todos()]

    def buscar(self, id):
        return self._obter(id).to_dict()

    def criar(self, dados):
        valores = self._validar(dados)
        entidade = self._montar(valores)
        return self._salvar(entidade)

    def atualizar(self, id, dados):
        entidade = self._obter(id)
        # PUT parcial: o que não vier no JSON mantém o valor atual
        mesclado = {
            campo: dados.get(campo, getattr(entidade, campo))
            for campo in type(entidade).CAMPOS_EDITAVEIS
        }
        valores = self._validar(mesclado, id_atual=id)
        self._aplicar(entidade, valores)
        return self._salvar(entidade)

    def deletar(self, id):
        entidade = self._obter(id)
        self._antes_de_excluir(entidade)
        try:
            self._repo.excluir(entidade)
        except IntegrityError:
            # rede de segurança: o banco (ON DELETE RESTRICT) também barra
            raise RegraNegocioError(self._MSG_EXCLUSAO_BLOQUEADA)

    # ---------- ganchos que as filhas sobrescrevem ----------
    def _validar(self, dados, id_atual=None):
        raise NotImplementedError

    def _montar(self, valores):
        return self._ENTIDADE(**valores)

    def _aplicar(self, entidade, valores):
        for campo, valor in valores.items():
            setattr(entidade, campo, valor)

    def _antes_de_excluir(self, entidade):
        pass

    # ---------- internos ----------
    def _obter(self, id):
        entidade = self._repo.buscar_por_id(id)
        if entidade is None:
            raise NaoEncontradoError(self._MSG_NAO_ENCONTRADO)
        return entidade

    def _salvar(self, entidade):
        try:
            return self._repo.salvar(entidade).to_dict()
        except IntegrityError:
            raise RegraNegocioError(self._MSG_INTEGRIDADE)
