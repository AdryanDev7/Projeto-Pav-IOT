from typing import List

from fastapi import APIRouter, Depends

from entities.schemas import OperadorIn, OperadorOut
from routes.dependencies import get_operador, get_operador_controller

router = APIRouter(prefix="/operadores", tags=["Operadores"])


# IMPORTANTE: esta rota vem antes de "/{operador_id}", senão "login" seria lido como id.
@router.get("/login", response_model=List[OperadorOut])
def opcoes_de_login(ctrl=Depends(get_operador_controller)):
    """Sem autenticação: alimenta a tela de login da interface (simplificação didática)."""
    return ctrl.listar_para_login()


@router.get("", response_model=List[OperadorOut])
def listar(ctrl=Depends(get_operador_controller), operador=Depends(get_operador)):
    return ctrl.listar(operador)


@router.get("/{operador_id}", response_model=OperadorOut)
def buscar(operador_id: int, ctrl=Depends(get_operador_controller), operador=Depends(get_operador)):
    return ctrl.buscar(operador_id, operador)


@router.post("", response_model=OperadorOut, status_code=201)
def criar(dados: OperadorIn, ctrl=Depends(get_operador_controller), operador=Depends(get_operador)):
    return ctrl.criar(dados, operador)


@router.put("/{operador_id}", response_model=OperadorOut)
def atualizar(operador_id: int, dados: OperadorIn, ctrl=Depends(get_operador_controller),
              operador=Depends(get_operador)):
    return ctrl.atualizar(operador_id, dados, operador)


@router.delete("/{operador_id}", status_code=204)
def remover(operador_id: int, ctrl=Depends(get_operador_controller), operador=Depends(get_operador)):
    ctrl.remover(operador_id, operador)
