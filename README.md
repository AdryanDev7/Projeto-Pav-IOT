# Sistema de Análise de Dados de Sensores IoT

Dois projetos separados (exigência do enunciado):

- `projeto_API/`  API FastAPI + PostgreSQL, dockerizada
- `interface/`    Interface Tkinter, roda FORA do Docker

## Subir a API (qualquer máquina com Docker)
    cd projeto_API
    docker compose up --build
    # Swagger: http://localhost:8000/docs
    # Recriar banco do zero: docker compose down -v && docker compose up --build

## Rodar a interface
    cd interface
    pip install -r requirements.txt
    python main.py          # (no Linux pode precisar: sudo apt install python3-tk)

## Usuários de teste (criados pelo init.sql)
| id | nome              | perfil     | zona          |
|----|-------------------|------------|---------------|
| 1  | Carlos Supervisor | SUPERVISOR | ADMINISTRACAO |
| 2  | Ana Operadora     | OPERADOR   | ZONA_A        |
| 3  | Bruno Operador    | OPERADOR   | ZONA_B        |

## Sensores de teste
| id | nome               | zona   | limite | observação                         |
|----|--------------------|--------|--------|------------------------------------|
| 1  | Temp Caldeira 01   | ZONA_A | 80     | aferido há 10 dias                 |
| 2  | Umidade Estoque 01 | ZONA_A | 85     |                                    |
| 3  | Temp Forno 02      | ZONA_B | 100    | atuador VÁLVULA                    |
| 4  | Pressao Linha 03   | ZONA_B | 900    | instalado há 200 dias (calibração) |
| 5  | Temp Demo Watchdog | ZONA_A | 80     | intervalo 5 s (fica OFFLINE rápido)|

## Variáveis de demonstração (docker-compose.yml)
AGREGACAO_SEGUNDOS=30 (enunciado: 300), SEGUNDOS_ESCALONAMENTO=60 (enunciado: 900),
INTERVALO_JOBS_SEGUNDOS=10 (rotinas de watchdog/escalonamento).

## Logs (pasta projeto_API/logs)
leituras_rejeitadas.log (regra 1), notificacoes.log (regra 9), eventos.log (alertas/watchdog/atuadores)
