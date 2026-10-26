from typing import List

from fastapi import APIRouter, Depends

from entities.schemas import AlertaIn, AlertaOut, AlertaUpdate
from routes.dependencies import get_alerta_controller, get_operador

router = APIRouter(prefix="/alertas", tags=["Alertas"])


@router.get("", response_model=List[AlertaOut])
def listar(ctrl=Depends(get_alerta_controller), operador=Depends(get_operador)):
    return ctrl.listar(operador)


@router.get("/{alerta_id}", response_model=AlertaOut)
def buscar(alerta_id: int, ctrl=Depends(get_alerta_controller), operador=Depends(get_operador)):
    return ctrl.buscar(alerta_id, operador)


@router.post("", response_model=AlertaOut, status_code=201)
def criar(dados: AlertaIn, ctrl=Depends(get_alerta_controller), operador=Depends(get_operador)):
    return ctrl.criar(dados, operador)


@router.post("/{alerta_id}/reconhecer", response_model=AlertaOut)
def reconhecer(alerta_id: int, ctrl=Depends(get_alerta_controller), operador=Depends(get_operador)):
    """Reconhece o alerta no painel e evita o escalonamento (regra 9)."""
    return ctrl.reconhecer(alerta_id, operador)


@router.put("/{alerta_id}", response_model=AlertaOut)
def atualizar(alerta_id: int, dados: AlertaUpdate, ctrl=Depends(get_alerta_controller),
              operador=Depends(get_operador)):
    return ctrl.atualizar(alerta_id, dados, operador)


@router.delete("/{alerta_id}", status_code=204)
def remover(alerta_id: int, ctrl=Depends(get_alerta_controller), operador=Depends(get_operador)):
    ctrl.remover(alerta_id, operador)
