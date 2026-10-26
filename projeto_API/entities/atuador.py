"""Classes de domínio do Atuador (regra 6).
Não é tabela: o tipo e o estado ficam em colunas do Sensor. A classe existe para
mostrar herança, polimorfismo e encapsulamento."""
from abc import ABC, abstractmethod

ESTADOS_ATUADOR = {
    "RELE": ("LIGADO", "DESLIGADO"),
    "VALVULA": ("ABERTA", "FECHADA"),
}


class Atuador(ABC):
    def __init__(self, sensor):
        self._sensor = sensor            # atributo protegido (encapsulamento)

    @property
    def estado(self) -> str:
        return self._sensor.atuador_estado

    @abstractmethod
    def desligar(self) -> str:
        """Comando de segurança. Cada subclasse implementa do seu jeito."""

    @abstractmethod
    def religar(self) -> str:
        ...


class AtuadorRele(Atuador):
    def desligar(self) -> str:
        self._sensor.atuador_estado = "DESLIGADO"
        return f"Relé do sensor '{self._sensor.nome}' DESLIGADO: alimentação cortada"

    def religar(self) -> str:
        self._sensor.atuador_estado = "LIGADO"
        return f"Relé do sensor '{self._sensor.nome}' LIGADO"


class AtuadorValvula(Atuador):
    def desligar(self) -> str:
        self._sensor.atuador_estado = "FECHADA"
        return f"Válvula do sensor '{self._sensor.nome}' FECHADA"

    def religar(self) -> str:
        self._sensor.atuador_estado = "ABERTA"
        return f"Válvula do sensor '{self._sensor.nome}' ABERTA"


_TIPOS = {"RELE": AtuadorRele, "VALVULA": AtuadorValvula}


def criar_atuador(sensor) -> Atuador:
    """Factory: devolve a subclasse certa conforme sensor.atuador_tipo."""
    return _TIPOS[sensor.atuador_tipo](sensor)
