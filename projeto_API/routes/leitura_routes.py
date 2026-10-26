from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from entities.schemas import LeituraIn, LeituraOut, RegistroLeituraOut
from routes.dependencies import get_leitura_controller, get_operador

router = APIRouter(prefix="/leituras", tags=["Leituras (telemetria)"])


@router.post("", response_model=RegistroLeituraOut, status_code=201)
def registrar(dados: LeituraIn, ctrl=Depends(get_leitura_controller)):
    """Endpoint usado pelo sensor/dispositivo (sem operador). Executa todo o pipeline de regras."""
    return ctrl.registrar(dados)


@router.get("", response_model=List[LeituraOut])
def listar(sensor_id: Optional[int] = None, limite: int = Query(100, ge=1, le=1000),
           ctrl=Depends(get_leitura_controller), operador=Depends(get_operador)):
    return ctrl.listar(operador, sensor_id, limite)


@router.get("/{leitura_id}", response_model=LeituraOut)
def buscar(leitura_id: int, ctrl=Depends(get_leitura_controller), operador=Depends(get_operador)):
    return ctrl.buscar(leitura_id, operador)


# REGRA 8: as rotas existem (o enunciado pede PUT/DELETE), mas SEMPRE respondem 405.
@router.api_route("/{leitura_id}", methods=["PUT", "PATCH", "DELETE"], include_in_schema=True)
def proibido(leitura_id: int, ctrl=Depends(get_leitura_controller)):
    ctrl.bloquear_alteracao()
