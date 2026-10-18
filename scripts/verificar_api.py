"""
Verificação ponta a ponta da API (CRUD, regras de negócio e cascatas).

Uso (com a API rodando):
    python scripts/verificar_api.py
    python scripts/verificar_api.py http://127.0.0.1:5000/api

Cria os próprios dados de teste e apaga tudo no final.
"""
import sys
import uuid
from datetime import datetime, timedelta

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000/api"
falhas = 0


def checar(nome, condicao, detalhe=""):
    global falhas
    if condicao:
        print(f"[OK]    {nome}")
    else:
        falhas += 1
        print(f"[FALHA] {nome}  -> {detalhe}")


def chamar(metodo, caminho, **kwargs):
    return requests.request(metodo, f"{BASE}{caminho}", timeout=10, **kwargs)


def erro_de(resp):
    try:
        return resp.json().get("erro", "")
    except ValueError:
        return ""


sufixo = uuid.uuid4().hex[:6].upper()
MSG_RN10 = "Não é possível excluir esta localização pois existem sensores associados."

# ---------------- Localizações ----------------
r = chamar("POST", "/localizacoes", json={"nome": "Fábrica Teste", "setor": "A", "latitude": -22.9, "longitude": -43.2})
checar("POST localização válida -> 201", r.status_code == 201, r.text)
loc_id = r.json().get("id")

r = chamar("POST", "/localizacoes", json={"nome": "X", "setor": "A", "latitude": 120, "longitude": 0})
checar("RN01 latitude 120 -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/localizacoes", json={"nome": "X", "setor": "A", "latitude": 0, "longitude": 200})
checar("RN01 longitude 200 -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/localizacoes", json={"setor": "A", "latitude": 0, "longitude": 0})
checar("RN07 sem 'nome' -> 400", r.status_code == 400 and "nome" in erro_de(r), r.text)
r = chamar("POST", "/localizacoes", data="isso não é json", headers={"Content-Type": "application/json"})
checar("corpo inválido -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/localizacoes", json={"nome": "X", "setor": "A", "latitude": "abc", "longitude": 0})
checar("latitude não numérica -> 400", r.status_code == 400, r.text)

r = chamar("GET", f"/localizacoes/{loc_id}")
checar("GET localização por id -> 200", r.status_code == 200 and r.json()["nome"] == "Fábrica Teste", r.text)
r = chamar("GET", "/localizacoes/999999")
checar("GET localização inexistente -> 404", r.status_code == 404, r.text)
r = chamar("PUT", f"/localizacoes/{loc_id}", json={"nome": "Fábrica Teste 2"})
checar("PUT parcial localização -> 200", r.status_code == 200 and r.json()["dados"]["nome"] == "Fábrica Teste 2", r.text)
r = chamar("PUT", "/localizacoes/999999", json={"nome": "Z"})
checar("PUT localização inexistente -> 404", r.status_code == 404, r.text)
r = chamar("GET", "/localizacoes")
checar("GET lista de localizações", r.status_code == 200 and any(x["id"] == loc_id for x in r.json()), r.text)

# ---------------- Sensores ----------------
serial = f"TEMP-{sufixo}"
r = chamar("POST", "/sensores", json={"codigo_serial": serial, "tipo": "Temperatura", "localizacao_id": loc_id, "nivel_bateria": 80})
checar("POST sensor válido -> 201", r.status_code == 201, r.text)
sensor_id = r.json().get("id")

r = chamar("POST", "/sensores", json={"codigo_serial": serial, "tipo": "T", "localizacao_id": loc_id, "nivel_bateria": 80})
checar("RN02 serial repetido -> 400", r.status_code == 400 and "serial" in erro_de(r), r.text)
r = chamar("POST", "/sensores", json={"codigo_serial": f"N-{sufixo}", "tipo": "T", "localizacao_id": 999999, "nivel_bateria": 80})
checar("RN03 localização inexistente -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/sensores", json={"codigo_serial": f"B-{sufixo}", "tipo": "T", "localizacao_id": loc_id, "nivel_bateria": 150})
checar("RN04 bateria 150 -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/sensores", json={"codigo_serial": f"S-{sufixo}", "tipo": "T", "localizacao_id": loc_id, "nivel_bateria": 50, "status": "xpto"})
checar("RN05 status inválido -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/sensores", json={"codigo_serial": f"V-{sufixo}", "tipo": "T", "nivel_bateria": 50})
checar("RN07 sem localizacao_id -> 400", r.status_code == 400, r.text)

r = chamar("PUT", f"/sensores/{sensor_id}", json={"codigo_serial": serial, "nivel_bateria": 70})
checar("PUT sensor mantendo o próprio serial -> 200", r.status_code == 200, r.text)
r = chamar("GET", f"/sensores/{sensor_id}")
checar("GET sensor por id -> 200", r.status_code == 200 and r.json()["nivel_bateria"] == 70, r.text)

# ---------------- RN10 ----------------
r = chamar("DELETE", f"/localizacoes/{loc_id}")
checar("RN10 excluir localização com sensor -> 400", r.status_code == 400, f"{r.status_code} {r.text}")
checar("RN10 mensagem exata", erro_de(r) == MSG_RN10, r.text)
r = chamar("GET", f"/sensores/{sensor_id}")
checar("RN10 sensor continua ligado à localização", r.status_code == 200 and r.json()["localizacao_id"] == loc_id, r.text)

# ---------------- Leituras e anomalias ----------------
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 50.5, "nivel_bateria": 80})
checar("POST leitura normal -> 201", r.status_code == 201, r.text)
leitura_normal = r.json().get("id")
r = chamar("GET", "/anomalias")
checar("leitura normal não gera anomalia", not any(a["leitura_id"] == leitura_normal for a in r.json()), r.text)

r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 95, "nivel_bateria": 80})
checar("POST leitura 95 -> 201", r.status_code == 201, r.text)
leitura_alta = r.json().get("id")
anoms = [a for a in chamar("GET", "/anomalias").json() if a["leitura_id"] == leitura_alta]
checar("RN08 valor > 90 gera 1 anomalia Crítica", len(anoms) == 1 and anoms[0]["severidade"] == "Crítica", anoms)

r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 40, "nivel_bateria": 10})
checar("POST leitura bateria 10% -> 201", r.status_code == 201, r.text)
leitura_bat = r.json().get("id")
anoms = [a for a in chamar("GET", "/anomalias").json() if a["leitura_id"] == leitura_bat]
checar("RN12 bateria < 15 gera anomalia Média", len(anoms) == 1 and anoms[0]["severidade"] == "Média", anoms)

r = chamar("POST", "/leituras", json={"sensor_id": 999999, "valor": 10, "nivel_bateria": 50})
checar("RN06 sensor inexistente -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/leituras", json={"valor": 10, "nivel_bateria": 50})
checar("RN07 sem sensor_id -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 10, "nivel_bateria": 120})
checar("RN04 bateria 120 na leitura -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": "nan", "nivel_bateria": 50})
checar("valor NaN -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 99999999, "nivel_bateria": 50})
checar("valor fora da faixa da coluna -> 400", r.status_code == 400, r.text)
futuro = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 10, "nivel_bateria": 50, "data_hora": futuro})
checar("RN09 data no futuro -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 10, "nivel_bateria": 50, "data_hora": "ontem"})
checar("data em formato inválido -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 20, "nivel_bateria": 60, "data_hora": "2026-01-15 10:30:00"})
checar("RN09 data passada informada -> 201", r.status_code == 201, r.text)
leitura_antiga = r.json().get("id")
r = chamar("GET", f"/leituras/{leitura_antiga}")
checar("data_hora informada é preservada", r.status_code == 200 and r.json()["data_hora"] == "2026-01-15 10:30:00", r.text)

r = chamar("GET", f"/leituras?sensor_id={sensor_id}")
checar("filtro de leituras por sensor", r.status_code == 200 and len(r.json()) == 4, r.text)
r = chamar("GET", f"/leituras?sensor_id={sensor_id}&inicio=2026-01-01 00:00:00&fim=2026-02-01 00:00:00")
checar("filtro de leituras por período", r.status_code == 200 and [x["id"] for x in r.json()] == [leitura_antiga], r.text)
r = chamar("GET", "/leituras?sensor_id=abc")
checar("filtro com sensor_id inválido -> 400", r.status_code == 400, r.text)

# PUT de leitura recalcula anomalias
r = chamar("PUT", f"/leituras/{leitura_alta}", json={"valor": 10})
checar("PUT leitura -> 200", r.status_code == 200, r.text)
anoms = [a for a in chamar("GET", "/anomalias").json() if a["leitura_id"] == leitura_alta]
checar("PUT leitura 95->10 remove a anomalia", len(anoms) == 0, anoms)
r = chamar("PUT", f"/leituras/{leitura_alta}", json={"valor": 99})
anoms = [a for a in chamar("GET", "/anomalias").json() if a["leitura_id"] == leitura_alta]
checar("PUT leitura 10->99 recria a anomalia", len(anoms) == 1, anoms)

# RN11
r = chamar("PUT", f"/sensores/{sensor_id}", json={"status": "Em Manutenção"})
checar("PUT sensor para 'Em Manutenção' -> 200", r.status_code == 200, r.text)
r = chamar("POST", "/leituras", json={"sensor_id": sensor_id, "valor": 10, "nivel_bateria": 50})
checar("RN11 sensor em manutenção recusa leitura -> 400", r.status_code == 400, r.text)
chamar("PUT", f"/sensores/{sensor_id}", json={"status": "Ativo"})

# Anomalias CRUD
r = chamar("POST", "/anomalias", json={"leitura_id": leitura_normal, "descricao_alerta": "Anomalia manual", "severidade": "Baixa"})
checar("POST anomalia -> 201", r.status_code == 201, r.text)
anom_id = r.json().get("id")
r = chamar("POST", "/anomalias", json={"leitura_id": 999999, "descricao_alerta": "x", "severidade": "Baixa"})
checar("anomalia com leitura inexistente -> 400", r.status_code == 400, r.text)
r = chamar("POST", "/anomalias", json={"leitura_id": leitura_normal, "descricao_alerta": "x", "severidade": "Gravíssima"})
checar("anomalia com severidade inválida -> 400", r.status_code == 400, r.text)
r = chamar("PUT", f"/anomalias/{anom_id}", json={"severidade": "Alta"})
checar("PUT anomalia -> 200", r.status_code == 200 and r.json()["dados"]["severidade"] == "Alta", r.text)
r = chamar("GET", f"/anomalias/{anom_id}")
checar("GET anomalia por id -> 200", r.status_code == 200, r.text)
r = chamar("DELETE", f"/anomalias/{anom_id}")
checar("DELETE anomalia -> 200", r.status_code == 200, r.text)
r = chamar("DELETE", f"/anomalias/{anom_id}")
checar("DELETE anomalia inexistente -> 404", r.status_code == 404, r.text)

# Estatísticas
r = chamar("GET", f"/sensores/{sensor_id}/estatisticas")
est = r.json() if r.status_code == 200 else {}
checar("estatísticas do sensor", r.status_code == 200 and est["total_leituras"] == 4 and est["maximo"] == 99.0 and est["minimo"] == 20.0 and est["total_anomalias"] == 2, r.text)
r = chamar("GET", "/sensores/999999/estatisticas")
checar("estatísticas de sensor inexistente -> 404", r.status_code == 404, r.text)

# DELETE leitura
r = chamar("DELETE", f"/leituras/{leitura_bat}")
checar("DELETE leitura -> 200", r.status_code == 200, r.text)
anoms = [a for a in chamar("GET", "/anomalias").json() if a["leitura_id"] == leitura_bat]
checar("DELETE leitura apaga as anomalias dela", len(anoms) == 0, anoms)
r = chamar("DELETE", f"/leituras/{leitura_bat}")
checar("DELETE leitura inexistente -> 404", r.status_code == 404, r.text)

# ---------------- Cascata e limpeza ----------------
r = chamar("DELETE", f"/sensores/{sensor_id}")
checar("DELETE sensor -> 200", r.status_code == 200, r.text)
leituras_sensor = chamar("GET", f"/leituras?sensor_id={sensor_id}").json()
checar("DELETE sensor apaga as leituras dele", leituras_sensor == [], leituras_sensor)
anoms = [a for a in chamar("GET", "/anomalias").json() if a["leitura_id"] in (leitura_normal, leitura_alta)]
checar("DELETE sensor apaga as anomalias das leituras", anoms == [], anoms)

r = chamar("DELETE", f"/localizacoes/{loc_id}")
checar("RN10 sem sensores a localização é excluída -> 200", r.status_code == 200, r.text)
r = chamar("DELETE", f"/localizacoes/{loc_id}")
checar("DELETE localização já excluída -> 404", r.status_code == 404, r.text)
r = chamar("DELETE", f"/sensores/{sensor_id}")
checar("DELETE sensor já excluído -> 404", r.status_code == 404, r.text)

print()
if falhas:
    print(f"{falhas} verificação(ões) FALHARAM.")
    sys.exit(1)
print("Todas as verificações passaram.")
