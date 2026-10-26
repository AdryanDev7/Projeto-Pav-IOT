from typing import List

from fastapi import APIRouter, Depends

from entities.schemas import ManutencaoIn, ManutencaoOut
from routes.dependencies import get_manutencao_controller, get_operador

router = APIRouter(prefix="/manutencoes", tags=["Manutenções"])


@router.get("", response_model=List[ManutencaoOut])
def listar(ctrl=Depends(get_manutencao_controller), operador=Depends(get_operador)):
    return ctrl.listar(operador)


@router.get("/{manutencao_id}", response_model=ManutencaoOut)
def buscar(manutencao_id: int, ctrl=Depends(get_manutencao_controller), operador=Depends(get_operador)):
    return ctrl.buscar(manutencao_id, operador)


@router.post("", response_model=ManutencaoOut, status_code=201)
def criar(dados: ManutencaoIn, ctrl=Depends(get_manutencao_controller), operador=Depends(get_operador)):
    return ctrl.criar(dados, operador)


@router.put("/{manutencao_id}", response_model=ManutencaoOut)
def atualizar(manutencao_id: int, dados: ManutencaoIn, ctrl=Depends(get_manutencao_controller),
              operador=Depends(get_operador)):
    return ctrl.atualizar(manutencao_id, dados, operador)


@router.delete("/{manutencao_id}", status_code=204)
def remover(manutencao_id: int, ctrl=Depends(get_manutencao_controller), operador=Depends(get_operador)):
    ctrl.remover(manutencao_id, operador)
