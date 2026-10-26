"""Modelos SQLAlchemy: uma classe para cada tabela (5 tabelas)."""
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base
from config.settings import agora


class Operador(Base):
    __tablename__ = "operador"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    perfil = Column(String(20), nullable=False)   # OPERADOR | SUPERVISOR
    zona = Column(String(50), nullable=False)     # regra 10


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)                     # TEMPERATURA | UMIDADE | PRESSAO
    zona = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="NORMAL")  # NORMAL | ALERTA_CRITICO | OFFLINE
    ativo = Column(Boolean, nullable=False, default=True)
    intervalo_segundos = Column(Integer, nullable=False, default=300)
    limite_seguranca = Column(Float, nullable=False)
    instalado_em = Column(DateTime, nullable=False, default=agora)
    ultima_comunicacao = Column(DateTime)                          # heartbeat (regra 4)
    ultimo_valor = Column(Float)                                   # delta check (regra 2)
    ultimo_valor_em = Column(DateTime)
    leituras_acima_limite = Column(Integer, nullable=False, default=0)   # persistência (regra 3)
    atuador_tipo = Column(String(20), nullable=False, default="RELE")    # RELE | VALVULA
    atuador_estado = Column(String(20), nullable=False, default="LIGADO")

    leituras = relationship("Leitura", back_populates="sensor")   # SEM cascade: telemetria é imutável
    manutencoes = relationship("Manutencao", back_populates="sensor", cascade="all, delete-orphan")
    alertas = relationship("Alerta", back_populates="sensor", cascade="all, delete-orphan")


class Leitura(Base):
    __tablename__ = "leitura"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    valor = Column(Float, nullable=False)
    flag = Column(String(30), nullable=False, default="OK")    # OK | SUSPEITA_RUIDO | REQUER_CALIBRACAO
    agregada = Column(Boolean, nullable=False, default=False)  # True = média de 5 min (regra 5)
    registrada_em = Column(DateTime, nullable=False, default=agora)

    sensor = relationship("Sensor", back_populates="leituras")


class Manutencao(Base):
    __tablename__ = "manutencao"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    data_afericao = Column(DateTime, nullable=False, default=agora)
    descricao = Column(String(255))

    sensor = relationship("Sensor", back_populates="manutencoes")


class Alerta(Base):
    __tablename__ = "alerta"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    prioridade = Column(String(10), nullable=False, default="ALTA")
    status = Column(String(20), nullable=False, default="ABERTO")   # ABERTO | RECONHECIDO | ESCALONADO
    mensagem = Column(String(255))
    criado_em = Column(DateTime, nullable=False, default=agora)
    reconhecido_por = Column(Integer, ForeignKey("operador.id"))
    reconhecido_em = Column(DateTime)

    sensor = relationship("Sensor", back_populates="alertas")
