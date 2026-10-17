from datetime import datetime
from repositories.leitura_repository import LeituraRepository
from entities.models import LeituraSensor, Sensor, Anomalia
from config.database import db

class LeituraService:
    @staticmethod
    def criar_leitura(dados):
        # Regra de Negócio 1: O sensor associado tem de existir
        sensor_id = dados.get('sensor_id')
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise ValueError("O sensor informado não existe.")

        valor = dados.get('valor')
        nivel_bateria = dados.get('nivel_bateria')

        if valor is None or nivel_bateria is None:
            raise ValueError("O valor da leitura e o nível da bateria são obrigatórios.")

        # Regra de Negócio 2: Validação de bateria (entre 0 e 100%)
        if not (0 <= int(nivel_bateria) <= 100):
            raise ValueError("O nível da bateria tem de estar compreendido entre 0 e 100.")

        nova_leitura = LeituraSensor(
            sensor_id=sensor_id,
            valor=valor,
            nivel_bateria=nivel_bateria,
            data_hora=datetime.now()
        )
        
        LeituraRepository.salvar(nova_leitura)

        # Regra de Negócio 3 (Extra para Anomalias): Se o valor ultrapassar um limite crítico (ex: > 90), gera automaticamente uma anomalia
        if float(valor) > 90.0:
            anomalia = Anomalia(
                leitura_id=nova_leitura.id,
                descricao_alerta=f"Valor crítico detetado: {valor}",
                severidade="Alta"
            )
            db.session.add(anomalia)
            db.session.commit()

        return nova_leitura

    @staticmethod
    def listar_leituras():
        leituras = LeituraRepository.listar_todas()
        return [
            {
                "id": l.id,
                "sensor_id": l.sensor_id,
                "valor": float(l.valor),
                "nivel_bateria": l.nivel_bateria,
                "data_hora": l.data_hora.strftime("%Y-%m-%d %H:%M:%S")
            } for l in leituras
        ]

    @staticmethod
    def deletar_leitura(leitura_id):
        leitura = LeituraRepository.buscar_por_id(leitura_id)
        if not leitura:
            raise ValueError("Leitura não encontrada.")
        LeituraRepository.deletar(leitura)
        return True