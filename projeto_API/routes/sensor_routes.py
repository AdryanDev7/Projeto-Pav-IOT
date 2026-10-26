from typing import List

from fastapi import APIRouter, Depends

from entities.schemas import SensorIn, SensorOut
from routes.dependencies import get_operador, get_sensor_controller

router = APIRouter(prefix="/sensores", tags=["Sensores"])


@router.get("", response_model=List[SensorOut])
def listar(ctrl=Depends(get_sensor_controller), operador=Depends(get_operador)):
    return ctrl.listar(operador)


@router.get("/{sensor_id}", response_model=SensorOut)
def buscar(sensor_id: int, ctrl=Depends(get_sensor_controller), operador=Depends(get_operador)):
    return ctrl.buscar(sensor_id, operador)


@router.post("", response_model=SensorOut, status_code=201)
def criar(dados: SensorIn, ctrl=Depends(get_sensor_controller), operador=Depends(get_operador)):
    return ctrl.criar(dados, operador)


@router.put("/{sensor_id}", response_model=SensorOut)
def atualizar(sensor_id: int, dados: SensorIn, ctrl=Depends(get_sensor_controller),
              operador=Depends(get_operador)):
    return ctrl.atualizar(sensor_id, dados, operador)


@router.delete("/{sensor_id}", status_code=204)
def remover(sensor_id: int, ctrl=Depends(get_sensor_controller), operador=Depends(get_operador)):
    ctrl.remover(sensor_id, operador)
