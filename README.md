# Projeto PAV - Sistema de Análise de Dados de Sensores IoT (API)

API REST em Python (Flask-RESTful + Flask-SQLAlchemy) com PostgreSQL, em arquitetura de camadas e dockerizada.
A interface gráfica (Tkinter) é um projeto separado e roda fora do container.

## Como executar (sem instalar nada além do Docker)

```bash
docker compose up -d --build
```

- API: http://127.0.0.1:5000/api
- PostgreSQL: `localhost:5433` (usuário `postgres`, senha `postgres`, banco `iot_database`)
- O banco é inicializado pelo `init.sql`. Para recriar do zero: `docker compose down -v` e subir de novo.
- Verificação automática dos requisitos (com a API no ar): `python scripts/verificar_api.py`

## Arquitetura em camadas

| Pasta | Responsabilidade |
|---|---|
| `config/` | Conexão e inicialização do banco (`DATABASE_URL`) |
| `entities/` | Modelos SQLAlchemy (`EntidadeBase` abstrata + 4 entidades) |
| `repositories/` | Acesso ao banco (`BaseRepository` + um repositório por entidade) |
| `services/` | Regras de negócio e validações (`BaseService` + um service por entidade, detectores de anomalia, estatísticas) |
| `controllers/` | Recursos Flask-RESTful: recebem a requisição e devolvem JSON/HTTP |
| `routes/` | Registro dos endpoints e montagem das dependências |

Orientação a objetos: herança (`EntidadeBase`, `BaseRepository`, `BaseService`, `RecursoBase`), polimorfismo
(`to_dict`, `_validar`, `DetectorAnomalia.detectar`), construtores com injeção de dependência e encapsulamento
(atributos `_repo`, `_modelo`, `_service`, `_limite`).

## Modelo de dados (4 tabelas)

`localizacoes` 1—N `sensores` 1—N `leituras_sensores` 1—N `anomalias`

- `sensores.localizacao_id` → `ON DELETE RESTRICT`
- `leituras_sensores.sensor_id` e `anomalias.leitura_id` → `ON DELETE CASCADE`

## Endpoints (prefixo `/api`)

| Recurso | Endpoints |
|---|---|
| Localizações | `GET/POST /localizacoes` · `GET/PUT/DELETE /localizacoes/<id>` |
| Sensores | `GET/POST /sensores` · `GET/PUT/DELETE /sensores/<id>` · `GET /sensores/<id>/estatisticas?inicio=&fim=` |
| Leituras | `GET/POST /leituras` (filtros `sensor_id`, `inicio`, `fim`) · `GET/PUT/DELETE /leituras/<id>` |
| Anomalias | `GET/POST /anomalias` · `GET/PUT/DELETE /anomalias/<id>` |

Erros devolvem JSON `{"erro": "mensagem"}` com 400 (regra de negócio/dado inválido) ou 404 (não encontrado).

## Regras de negócio

1. **RN01** - Latitude entre -90 e 90; longitude entre -180 e 180.
2. **RN02** - `codigo_serial` único por sensor.
3. **RN03** - Sensor só pode ser cadastrado em uma localização existente.
4. **RN04** - Nível de bateria entre 0 e 100 (sensores e leituras).
5. **RN05** - Status do sensor: `Ativo`, `Inativo` ou `Em Manutenção`.
6. **RN06** - Leitura só pode ser registrada para um sensor existente.
7. **RN07** - Campos obrigatórios (e do tipo correto) em todos os cadastros.
8. **RN08** - Leitura com valor acima de 90.0 gera automaticamente uma anomalia de severidade **Crítica**.
9. **RN09** - Data/hora da leitura é gerada automaticamente quando não informada; datas no futuro são recusadas.
10. **RN10** - Deleção segura: não é possível excluir uma localização que possui sensores associados (HTTP 400).
11. **RN11** - Sensor que não está `Ativo` não aceita novas leituras.
12. **RN12** - Leitura com bateria abaixo de 15% gera uma anomalia de severidade **Média**.

Análise de dados: `GET /sensores/<id>/estatisticas` devolve total de leituras, média, mínimo, máximo,
desvio padrão e total de anomalias (com filtro opcional por período).
