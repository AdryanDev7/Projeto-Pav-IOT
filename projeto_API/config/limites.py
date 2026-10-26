"""Limites físicos e variações máximas por tipo de sensor (regras 1 e 2)."""

# (mínimo, máximo) que o equipamento consegue medir
LIMITES_FISICOS = {
    "TEMPERATURA": (-50.0, 150.0),   # °C
    "UMIDADE": (0.0, 100.0),         # %
    "PRESSAO": (300.0, 1100.0),      # hPa
}

# Maior salto aceitável entre duas leituras consecutivas dentro da janela curta
DELTA_MAXIMO = {
    "TEMPERATURA": 30.0,
    "UMIDADE": 40.0,
    "PRESSAO": 100.0,
}

UNIDADES = {"TEMPERATURA": "°C", "UMIDADE": "%", "PRESSAO": "hPa"}
