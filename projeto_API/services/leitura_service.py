"""Pipeline de ingestão de telemetria. É aqui que moram as regras 1, 2, 3, 5, 6, 7 e 8.

Ordem do pipeline em registrar():
  1. sensor existe e está ativo
  2. REGRA 1  limites físicos            -> 422 + log
  3. REGRA 2  delta check (ruído)        -> flag SUSPEITA_RUIDO
  4. REGRA 4  heartbeat (volta de OFFLINE)
  5. REGRA 3  persistência do alerta     -> ALERTA_CRITICO
  6. REGRA 6  atuador desliga            -> Atuador.desligar()
  7. REGRA 7  calibração                 -> flag REQUER_CALIBRACAO
  8. REGRA 5  throttling                 -> média de 5 min ou gravação direta
"""
import logging
import threading
from datetime import timedelta
from statistics import mean

from config import settings
from config.excecoes import (ConflitoErro, NaoEncontradoErro,
                             OperacaoNaoPermitidaErro, RegraVioladaErro)
from config.limites import DELTA_MAXIMO, LIMITES_FISICOS, UNIDADES
from config.settings import agora
from entities.atuador import criar_atuador
from entities.models import Alerta, Leitura
from services.autorizacao import exigir_zona, zona_do_operador

log_rejeitadas = logging.getLogger("iot.rejeitadas")
log_eventos = logging.getLogger("iot.eventos")


class LeituraService:
    # Buffer compartilhado entre requisições (atributo de CLASSE): sensor_id -> pacote.
    # Limitação conhecida: se a API reiniciar, o que estava acumulado se perde.
    _buffer: dict = {}
    _trava = threading.Lock()

    def __init__(self, leituras, sensores, alertas, manutencoes):
        self._leituras = leituras
        self._sensores = sensores
        self._alertas = alertas
        self._manutencoes = manutencoes

    # ------------------------------------------------------------ ingestão
    def registrar(self, dados):
        sensor = self._sensor_ou_404(dados.sensor_id)
        if not sensor.ativo:
            raise ConflitoErro(f"O sensor '{sensor.nome}' está desativado e não aceita leituras.")

        valor = dados.valor
        self._validar_limites_fisicos(sensor, valor)               # regra 1

        momento = agora()
        eventos = []
        flag = self._classificar_ruido(sensor, valor, momento)     # regra 2
        self._atualizar_heartbeat(sensor, momento, eventos)        # regra 4

        if flag == "OK":
            sensor.ultimo_valor = valor
            sensor.ultimo_valor_em = momento
            self._avaliar_persistencia(sensor, valor, eventos)     # regras 3 e 6
            if self._requer_calibracao(sensor, momento):           # regra 7
                flag = "REQUER_CALIBRACAO"
                eventos.append("Sensor sem aferição há mais de "
                               f"{settings.DIAS_CALIBRACAO} dias: leitura marcada REQUER_CALIBRACAO")
        else:
            eventos.append("Salto abrupto detectado: leitura marcada SUSPEITA_RUIDO "
                           "e excluída das médias oficiais")

        leitura = self._persistir(sensor, valor, flag, momento)    # regra 5
        self._sensores.confirmar()                                 # um único commit para tudo
        if leitura is not None:
            self._leituras.recarregar(leitura)

        if leitura is not None:
            mensagem = "Leitura gravada no banco."
        else:
            mensagem = (f"Leitura recebida e acumulada para a média de "
                        f"{settings.AGREGACAO_SEGUNDOS}s (ainda não gravada).")
        return {"persistida": leitura is not None, "mensagem": mensagem, "flag": flag,
                "status_sensor": sensor.status, "eventos": eventos, "leitura": leitura}

    # ----------------------------------------------------- consultas
    def listar(self, operador, sensor_id=None, limite=100):
        if sensor_id is not None:
            exigir_zona(operador, self._sensor_ou_404(sensor_id).zona)
        return self._leituras.listar_filtrado(
            sensor_id=sensor_id, zona=zona_do_operador(operador), limite=limite)

    def buscar(self, id_, operador):
        leitura = self._leituras.buscar(id_)
        if leitura is None:
            raise NaoEncontradoErro(f"Leitura {id_} não encontrada.")
        exigir_zona(operador, leitura.sensor.zona)
        return leitura

    # ------------------------------------------------------ regra 8
    def bloquear_alteracao(self):
        log_eventos.warning("Tentativa de alterar/excluir telemetria bloqueada (regra 8)")
        raise OperacaoNaoPermitidaErro(
            "Operação proibida: leituras de telemetria são imutáveis (log auditável). "
            "Não é possível alterar nem excluir dados históricos.")

    # ------------------------------------------------------ regras (privados)
    def _sensor_ou_404(self, sensor_id):
        sensor = self._sensores.buscar(sensor_id)
        if sensor is None:
            raise NaoEncontradoErro(f"Sensor {sensor_id} não encontrado.")
        return sensor

    def _validar_limites_fisicos(self, sensor, valor):
        """REGRA 1: rejeita valor impossível para o equipamento, com HTTP 422 e log."""
        minimo, maximo = LIMITES_FISICOS[sensor.tipo]
        if not (minimo <= valor <= maximo):
            log_rejeitadas.warning(
                f"REJEITADA sensor_id={sensor.id} tipo={sensor.tipo} valor={valor} "
                f"(faixa válida {minimo} a {maximo})")
            raise RegraVioladaErro(
                f"Valor {valor}{UNIDADES[sensor.tipo]} fora do intervalo físico suportado "
                f"({minimo} a {maximo}{UNIDADES[sensor.tipo]}) para sensor de {sensor.tipo}. "
                "A tentativa foi registrada no log.")

    def _classificar_ruido(self, sensor, valor, momento) -> str:
        """REGRA 2: compara com a última leitura VÁLIDA dentro de uma janela curta."""
        if sensor.ultimo_valor is None or sensor.ultimo_valor_em is None:
            return "OK"
        segundos = (momento - sensor.ultimo_valor_em).total_seconds()
        salto = abs(valor - sensor.ultimo_valor)
        if segundos <= settings.JANELA_DELTA_SEGUNDOS and salto > DELTA_MAXIMO[sensor.tipo]:
            return "SUSPEITA_RUIDO"
        return "OK"

    def _atualizar_heartbeat(self, sensor, momento, eventos):
        """REGRA 4 (lado da API): cada leitura atualiza o carimbo; sensor OFFLINE volta ao ar."""
        sensor.ultima_comunicacao = momento
        if sensor.status == "OFFLINE":
            sensor.status = "NORMAL"
            sensor.leituras_acima_limite = 0
            eventos.append("Sensor voltou a comunicar: OFFLINE -> NORMAL")

    def _avaliar_persistencia(self, sensor, valor, eventos):
        """REGRA 3: só vira ALERTA_CRITICO após N leituras consecutivas acima do limite."""
        if valor > sensor.limite_seguranca:
            sensor.leituras_acima_limite += 1
            eventos.append(f"Leitura acima do limite ({sensor.leituras_acima_limite}/"
                           f"{settings.PERSISTENCIA_LEITURAS})")
            if (sensor.leituras_acima_limite >= settings.PERSISTENCIA_LEITURAS
                    and sensor.status != "ALERTA_CRITICO"):
                sensor.status = "ALERTA_CRITICO"
                self._disparar_protecao(sensor, eventos)
        else:
            sensor.leituras_acima_limite = 0
            if sensor.status == "ALERTA_CRITICO":
                sensor.status = "NORMAL"
                eventos.append("Valores normalizados: ALERTA_CRITICO -> NORMAL")

    def _disparar_protecao(self, sensor, eventos):
        """REGRA 6: evento interno -> abre alerta e comanda o Atuador (polimorfismo)."""
        self._alertas.adicionar(Alerta(
            sensor_id=sensor.id, prioridade="ALTA", status="ABERTO",
            mensagem=f"Sensor '{sensor.nome}' acima de {sensor.limite_seguranca} "
                     f"por {settings.PERSISTENCIA_LEITURAS} leituras consecutivas"))
        acao = criar_atuador(sensor).desligar()      # RELE ou VALVULA, cada um do seu jeito
        eventos.append("ALERTA_CRITICO confirmado: alerta de prioridade ALTA aberto")
        eventos.append(f"Comando de segurança enviado: {acao}")
        log_eventos.critical(f"ALERTA_CRITICO sensor_id={sensor.id} | {acao}")

    def _requer_calibracao(self, sensor, momento) -> bool:
        """REGRA 7: mais de 180 dias desde a última aferição (ou desde a instalação)."""
        ultima = self._manutencoes.ultima_afericao(sensor.id)
        referencia = ultima.data_afericao if ultima else sensor.instalado_em
        return (momento - referencia) > timedelta(days=settings.DIAS_CALIBRACAO)

    # ----------------------------------------------------- regra 5
    def _persistir(self, sensor, valor, flag, momento):
        """REGRA 5: normal -> grava só a média a cada 5 min; alerta -> grava cada leitura."""
        em_alerta = sensor.status == "ALERTA_CRITICO"
        if em_alerta:
            self._descarregar_parcial(sensor, momento)    # não perde o que estava acumulado
        if em_alerta or flag == "SUSPEITA_RUIDO":
            return self._gravar(sensor, valor, flag, momento, agregada=False)

        with self._trava:
            pacote = self._buffer.setdefault(
                sensor.id, {"valores": [], "inicio": momento, "flag": "OK"})
            pacote["valores"].append(valor)
            if flag == "REQUER_CALIBRACAO":
                pacote["flag"] = flag
            if (momento - pacote["inicio"]).total_seconds() < settings.AGREGACAO_SEGUNDOS:
                return None                               # ainda acumulando
            del self._buffer[sensor.id]
        return self._gravar(sensor, mean(pacote["valores"]), pacote["flag"], momento, agregada=True)

    def _descarregar_parcial(self, sensor, momento):
        with self._trava:
            pacote = self._buffer.pop(sensor.id, None)
        if pacote and pacote["valores"]:
            self._gravar(sensor, mean(pacote["valores"]), pacote["flag"], momento, agregada=True)

    def _gravar(self, sensor, valor, flag, momento, agregada):
        leitura = Leitura(sensor_id=sensor.id, valor=round(valor, 3), flag=flag,
                          agregada=agregada, registrada_em=momento)
        self._leituras.adicionar(leitura)
        return leitura
