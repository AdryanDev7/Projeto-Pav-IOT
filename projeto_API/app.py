"""Ponto de entrada da API. Rodar local: uvicorn app:app --reload"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

import entities.models  # noqa: F401  (registra os modelos no metadata)
from config.database import Base, engine
from config.excecoes import ErroNegocio
from config.logging_config import configurar_logs
from routes import (alerta_routes, analise_routes, leitura_routes, manutencao_routes,
                    operador_routes, sensor_routes)
from services.agendador import criar_agendador


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    configurar_logs()
    Base.metadata.create_all(engine)      # não faz nada se o init.sql já criou as tabelas
    agendador = criar_agendador()
    agendador.start()                     # watchdog (regra 4) e escalonamento (regra 9)
    yield
    agendador.shutdown()


app = FastAPI(title="API de Monitoramento de Sensores IoT", version="1.0.0", lifespan=ciclo_de_vida)


@app.exception_handler(ErroNegocio)
async def tratar_erro_negocio(request: Request, erro: ErroNegocio):
    return JSONResponse(status_code=erro.status_code, content={"detail": erro.mensagem})


@app.exception_handler(IntegrityError)
async def tratar_integridade(request: Request, erro: IntegrityError):
    return JSONResponse(status_code=409, content={
        "detail": "Operação violaria a integridade dos dados (o registro é referenciado por outros)."})


for modulo in (operador_routes, sensor_routes, analise_routes, leitura_routes,
               manutencao_routes, alerta_routes):
    app.include_router(modulo.router)


@app.get("/", tags=["Saúde"])
def raiz():
    return {"status": "online", "documentacao": "/docs"}
