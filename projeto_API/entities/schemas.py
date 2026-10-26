"""Schemas Pydantic: validam o que ENTRA (…In) e formatam o que SAI (…Out) da API."""
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class EntradaBase(BaseModel):
    """Base de todos os schemas de entrada: remove espaços das pontas dos textos."""
    model_config = ConfigDict(str_strip_whitespace=True)


class SaidaBase(BaseModel):
    """Base de todos os schemas de saída: permite ler direto de objetos SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------- Operador
class OperadorIn(EntradaBase):
    nome: str = Field(min_length=2, max_length=100)
    perfil: Literal["OPERADOR", "SUPERVISOR"]
    zona: str = Field(min_length=1, max_length=50)


class OperadorOut(SaidaBase):
    id: int
    nome: str
    perfil: str
    zona: str


# ------------------------------------------------------------------ Sensor
class SensorIn(EntradaBase):
    nome: str = Field(min_length=2, max_length=100)
    tipo: Literal["TEMPERATURA", "UMIDADE", "PRESSAO"]
    zona: str = Field(min_length=1, max_length=50)
    limite_seguranca: float = Field(allow_inf_nan=False)
    intervalo_segundos: int = Field(default=300, gt=0)
    ativo: bool = True
    atuador_tipo: Literal["RELE", "VALVULA"] = "RELE"
    atuador_estado: Optional[Literal["LIGADO", "DESLIGADO", "ABERTA", "FECHADA"]] = None
    instalado_em: Optional[datetime] = None


class SensorOut(SaidaBase):
    id: int
    nome: str
    tipo: str
    zona: str
    status: str
    ativo: bool
    intervalo_segundos: int
    limite_seguranca: float
    instalado_em: datetime
    ultima_comunicacao: Optional[datetime] = None
    ultimo_valor: Optional[float] = None
    leituras_acima_limite: int
    atuador_tipo: str
    atuador_estado: str


# ----------------------------------------------------------------- Leitura
class LeituraIn(EntradaBase):
    sensor_id: int
    valor: float = Field(allow_inf_nan=False)


class LeituraOut(SaidaBase):
    id: int
    sensor_id: int
    valor: float
    flag: str
    agregada: bool
    registrada_em: datetime


class RegistroLeituraOut(BaseModel):
    """Resposta do POST /leituras: conta o que o pipeline de regras fez."""
    persistida: bool
    mensagem: str
    flag: str
    status_sensor: str
    eventos: List[str] = []
    leitura: Optional[LeituraOut] = None


# -------------------------------------------------------------- Manutencao
class ManutencaoIn(EntradaBase):
    sensor_id: int
    data_afericao: Optional[datetime] = None
    descricao: Optional[str] = Field(default=None, max_length=255)


class ManutencaoOut(SaidaBase):
    id: int
    sensor_id: int
    data_afericao: datetime
    descricao: Optional[str] = None


# ------------------------------------------------------------------ Alerta
class AlertaIn(EntradaBase):
    sensor_id: int
    prioridade: Literal["ALTA", "MEDIA", "BAIXA"] = "ALTA"
    status: Literal["ABERTO", "RECONHECIDO", "ESCALONADO"] = "ABERTO"
    mensagem: Optional[str] = Field(default=None, max_length=255)


class AlertaUpdate(EntradaBase):
    prioridade: Literal["ALTA", "MEDIA", "BAIXA"]
    status: Literal["ABERTO", "RECONHECIDO", "ESCALONADO"]
    mensagem: Optional[str] = Field(default=None, max_length=255)


class AlertaOut(SaidaBase):
    id: int
    sensor_id: int
    prioridade: str
    status: str
    mensagem: Optional[str] = None
    criado_em: datetime
    reconhecido_por: Optional[int] = None
    reconhecido_em: Optional[datetime] = None


# ----------------------------------------------------------------- Análise
class EstatisticasOut(BaseModel):
    sensor_id: int
    sensor_nome: str
    tipo: str
    unidade: str
    inicio: Optional[datetime] = None
    fim: Optional[datetime] = None
    leituras_validas: int
    ruido_descartado: int
    media: Optional[float] = None
    minimo: Optional[float] = None
    maximo: Optional[float] = None
    desvio_padrao: Optional[float] = None


class AnomaliaItem(BaseModel):
    leitura_id: int
    valor: float
    z_score: float
    registrada_em: datetime


class AnomaliasOut(BaseModel):
    sensor_id: int
    limiar: float
    amostras: int
    media: Optional[float] = None
    desvio_padrao: Optional[float] = None
    anomalias: List[AnomaliaItem]
