from datetime import datetime, timedelta

from entities.leitura import LeituraSensor
from services import validadores
from services.base_service import BaseService
from services.detectores import DetectorLimiteValor, DetectorBateriaBaixa
from services.exceptions import RegraNegocioError

VALOR_MAXIMO = 999999.0  # a coluna é NUMERIC(10, 4)


class LeituraService(BaseService):
    _ENTIDADE = LeituraSensor
    _MSG_NAO_ENCONTRADO = "Leitura não encontrada."
    _MSG_INTEGRIDADE = "Violação de integridade: o sensor informado não existe."

    def __init__(self, repositorio, sensor_repositorio, detectores=None):
        super().__init__(repositorio)
        self._sensor_repo = sensor_repositorio
        # Lista de objetos de tipos diferentes tratados da mesma forma (POLIMORFISMO)
        self._detectores = detectores if detectores is not None else [
            DetectorLimiteValor(90.0),   # RN08
            DetectorBateriaBaixa(15),    # RN12
        ]

    def listar_filtrado(self, sensor_id=None, inicio=None, fim=None):
        if sensor_id not in (None, ""):
            sensor_id = validadores.inteiro({"sensor_id": sensor_id}, "sensor_id")
        else:
            sensor_id = None
        inicio = validadores.data_hora(inicio, "inicio") if inicio else None
        fim = validadores.data_hora(fim, "fim") if fim else None
        leituras = self._repo.listar_filtrado(sensor_id, inicio, fim)
        return [leitura.to_dict() for leitura in leituras]

    def _validar(self, dados, id_atual=None):
        validadores.exigir_campos(dados, ("sensor_id", "valor", "nivel_bateria"))  # RN07
        sensor_id = validadores.inteiro(dados, "sensor_id")
        valor = validadores.decimal(dados, "valor")
        bateria = validadores.inteiro(dados, "nivel_bateria")

        if abs(valor) > VALOR_MAXIMO:
            raise RegraNegocioError(f"O valor deve estar entre -{VALOR_MAXIMO:.0f} e {VALOR_MAXIMO:.0f}.")

        # RN04: bateria entre 0 e 100
        if not 0 <= bateria <= 100:
            raise RegraNegocioError("O nível de bateria deve estar entre 0 e 100.")

        # RN06: a leitura precisa pertencer a um sensor que existe
        sensor = self._sensor_repo.buscar_por_id(sensor_id)
        if sensor is None:
            raise RegraNegocioError("O sensor informado não existe.")

        # RN11: sensor que não está Ativo não aceita novas leituras
        if id_atual is None and sensor.status != "Ativo":
            raise RegraNegocioError(f"O sensor está '{sensor.status}' e não aceita novas leituras.")

        # RN09: carimbo de data/hora automático; datas no futuro são recusadas
        if dados.get("data_hora") in (None, ""):
            momento = datetime.now()
        else:
            momento = validadores.data_hora(dados["data_hora"], "data_hora")
            if momento > datetime.now() + timedelta(minutes=1):  # 1 min de tolerância de relógio
                raise RegraNegocioError("A data/hora da leitura não pode estar no futuro.")

        return {
            "sensor_id": sensor_id,
            "valor": valor,
            "nivel_bateria": bateria,
            "data_hora": momento,
        }

    def _montar(self, valores):
        leitura = LeituraSensor(**valores)
        self._anexar_anomalias(leitura)  # leitura e anomalias são gravadas no MESMO commit
        return leitura

    def _aplicar(self, leitura, valores):
        mudou = (
            float(leitura.valor) != valores["valor"]
            or leitura.nivel_bateria != valores["nivel_bateria"]
        )
        super()._aplicar(leitura, valores)
        if mudou:
            # Valor/bateria mudaram: recalcula as anomalias desta leitura
            leitura.anomalias.clear()
            self._anexar_anomalias(leitura)

    def _anexar_anomalias(self, leitura):
        for detector in self._detectores:
            anomalia = detector.detectar(leitura)
            if anomalia is not None:
                leitura.anomalias.append(anomalia)
