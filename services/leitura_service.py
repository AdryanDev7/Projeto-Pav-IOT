from repositories.leitura_repository import LeituraRepository
from repositories.anomalia_repository import AnomaliaRepository
from entities.leitura import LeituraSensor
from entities.anomalia import Anomalia
from datetime import datetime

class LeituraService:
    @staticmethod
    def listar_leituras():
        leituras = LeituraRepository.listar_todos()
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
    def criar_leitura(dados):
        data_hora_str = dados.get("data_hora")
        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S") if data_hora_str else datetime.utcnow()
        
        valor = float(dados.get("valor"))

        nova_leitura = LeituraSensor(
            sensor_id=dados.get("sensor_id"),
            valor=valor,
            nivel_bateria=dados.get("nivel_bateria"),
            data_hora=data_hora
        )
        LeituraRepository.salvar(nova_leitura)

        # REGRA DE NEGÓCIO: Se o valor ultrapassar 90.0, gera uma anomalia automática!
        if valor > 90.0:
            from config.database import db
            db.session.flush() # Garante que o ID da leitura foi gerado no banco
            
            nova_anomalia = Anomalia(
                leitura_id=nova_leitura.id,
                descricao_alerta=f"Alerta crítico: Valor {valor} ultrapassou o limite seguro de 90.0!",
                severidade="Crítica"
            )
            AnomaliaRepository.salvar(nova_anomalia)

        return nova_leitura

    @staticmethod
    def deletar_leitura(id):
        leitura = LeituraRepository.buscar_por_id(id)
        if not leitura:
            return False
        LeituraRepository.excluir(leitura)
        return True