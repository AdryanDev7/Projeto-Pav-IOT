"""Processamento/análise dos dados (exigido pelo enunciado: não é só CRUD)."""
from statistics import mean, pstdev

from config.excecoes import NaoEncontradoErro, RegraVioladaErro
from config.limites import UNIDADES
from services.autorizacao import exigir_zona


class AnaliseService:
    def __init__(self, leituras, sensores):
        self._leituras = leituras
        self._sensores = sensores

    def _sensor_autorizado(self, sensor_id, operador):
        sensor = self._sensores.buscar(sensor_id)
        if sensor is None:
            raise NaoEncontradoErro(f"Sensor {sensor_id} não encontrado.")
        exigir_zona(operador, sensor.zona)
        return sensor

    def estatisticas(self, sensor_id, operador, inicio=None, fim=None):
        sensor = self._sensor_autorizado(sensor_id, operador)
        if inicio and fim and inicio > fim:
            raise RegraVioladaErro("A data inicial não pode ser posterior à data final.")

        validas = self._leituras.validas_no_periodo(sensor_id, inicio, fim)   # sem SUSPEITA_RUIDO
        ruido = self._leituras.contar_ruido(sensor_id, inicio, fim)
        valores = [leitura.valor for leitura in validas]

        resultado = {"sensor_id": sensor.id, "sensor_nome": sensor.nome, "tipo": sensor.tipo,
                     "unidade": UNIDADES[sensor.tipo], "inicio": inicio, "fim": fim,
                     "leituras_validas": len(valores), "ruido_descartado": ruido}
        if valores:
            resultado.update(media=round(mean(valores), 3), minimo=min(valores),
                             maximo=max(valores), desvio_padrao=round(pstdev(valores), 3))
        return resultado

    def anomalias(self, sensor_id, operador, limiar=3.0):
        """Detecção estatística por z-score: |valor - média| / desvio > limiar.
        Observação: com n amostras o z-score máximo possível é (n-1)/raiz(n), então
        para limiar 3 são necessárias ao menos 11 amostras."""
        self._sensor_autorizado(sensor_id, operador)
        validas = self._leituras.validas_no_periodo(sensor_id)
        valores = [leitura.valor for leitura in validas]
        resposta = {"sensor_id": sensor_id, "limiar": limiar, "amostras": len(valores),
                    "media": None, "desvio_padrao": None, "anomalias": []}
        if len(valores) < 3:
            return resposta

        media, desvio = mean(valores), pstdev(valores)
        resposta["media"], resposta["desvio_padrao"] = round(media, 3), round(desvio, 3)
        if desvio == 0:
            return resposta
        for leitura in validas:
            z = (leitura.valor - media) / desvio
            if abs(z) > limiar:
                resposta["anomalias"].append({"leitura_id": leitura.id, "valor": leitura.valor,
                                              "z_score": round(z, 3),
                                              "registrada_em": leitura.registrada_em})
        return resposta
