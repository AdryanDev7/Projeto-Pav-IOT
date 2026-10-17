from repositories.sensor_repository import SensorRepository
from entities.sensor import Sensor

class SensorService:
    @staticmethod
    def listar_sensores():
        sensores = SensorRepository.listar_todos()
        return [
            {
                "id": s.id,
                "codigo_serial": s.codigo_serial,
                "tipo": s.tipo,
                "status": s.status,
                "localizacao_id": s.localizacao_id,
                "nivel_bateria": s.nivel_bateria
            } for s in sensores
        ]

    @staticmethod
    def criar_sensor(dados):
        novo_sensor = Sensor(
            codigo_serial=dados.get("codigo_serial"),
            tipo=dados.get("tipo"),
            status=dados.get("status", "Ativo"),
            localizacao_id=dados.get("localizacao_id"),
            nivel_bateria=dados.get("nivel_bateria")
        )
        SensorRepository.salvar(novo_sensor)
        return novo_sensor

    @staticmethod
    def atualizar_sensor(id, dados):
        sensor = SensorRepository.buscar_por_id(id)
        if not sensor:
            return None
        sensor.codigo_serial = dados.get("codigo_serial", sensor.codigo_serial)
        sensor.tipo = dados.get("tipo", sensor.tipo)
        sensor.status = dados.get("status", sensor.status)
        sensor.localizacao_id = dados.get("localizacao_id", sensor.localizacao_id)
        sensor.nivel_bateria = dados.get("nivel_bateria", sensor.nivel_bateria)
        SensorRepository.salvar(sensor)
        return sensor

    @staticmethod
    def deletar_sensor(id):
        sensor = SensorRepository.buscar_por_id(id)
        if not sensor:
            return False
        SensorRepository.excluir(sensor)
        return True