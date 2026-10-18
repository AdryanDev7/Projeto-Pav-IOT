from entities.anomalia import Anomalia


class DetectorAnomalia:
    """
    Classe-base (HERANÇA) dos detectores de anomalia.
    Cada filha sobrescreve detectar() com a sua regra (POLIMORFISMO):
    o LeituraService chama detector.detectar(leitura) sem saber qual regra está por trás.
    """

    def detectar(self, leitura):
        """Devolve uma Anomalia se a leitura for anormal; senão, None."""
        raise NotImplementedError("Cada detector deve implementar detectar().")


class DetectorLimiteValor(DetectorAnomalia):
    """RN08: valor acima do limite seguro gera anomalia de severidade Crítica."""

    def __init__(self, limite=90.0):
        self._limite = limite

    def detectar(self, leitura):
        valor = float(leitura.valor)
        if valor > self._limite:
            return Anomalia(
                descricao_alerta=f"Alerta crítico: Valor {valor} ultrapassou o limite seguro de {self._limite}!",
                severidade="Crítica",
            )
        return None


class DetectorBateriaBaixa(DetectorAnomalia):
    """RN12: bateria abaixo do mínimo gera anomalia de severidade Média."""

    def __init__(self, minimo=15):
        self._minimo = minimo

    def detectar(self, leitura):
        if leitura.nivel_bateria < self._minimo:
            return Anomalia(
                descricao_alerta=f"Bateria baixa: {leitura.nivel_bateria}% (mínimo recomendado: {self._minimo}%).",
                severidade="Média",
            )
        return None
