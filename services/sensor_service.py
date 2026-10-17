from repositories.sensor_repository import SensorRepository
from entities.models import Sensor, Localizacao

class SensorService:
    @staticmethod
    def criar_sensor(dados):
        # Regra de negócio: Verificar se a localização existe
        localizacao_id = dados.get('localizacao_id')
        localizacao = Localizacao.query.get(localizacao_id)
        if not localizacao:
            raise ValueError("A localização informada não existe.")

        # Regra de negócio: O nível de bateria inicial não pode ser zero ou negativo
        nivel_bateria = dados.get('nivel_bateria', 100)
        if nivel_bateria <= 0:
            raise ValueError("O sensor não pode ser cadastrado com bateria zerada ou negativa.")

        novo_sensor = Sensor(
            codigo_serial=dados.get('codigo_serial'),
            tipo=dados.get('tipo'),
            status=dados.get('status', 'Ativo'),
            localizacao_id=localizacao_id
        )
        return SensorRepository.salvar(novo_sensor)

    @staticmethod
    def listar_sensores():
        sensores = SensorRepository.listar_todos()
        return [
            {
                "id": s.id,
                "codigo_serial": s.codigo_serial,
                "tipo": s.tipo,
                "status": s.status,
                "localizacao_id": s.localizacao_id
            } for s in sensores
        ]

    @staticmethod
    def deletar_sensor(sensor_id):
        sensor = SensorRepository.buscar_por_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor não encontrado.")
        SensorRepository.deletar(sensor)
        return True