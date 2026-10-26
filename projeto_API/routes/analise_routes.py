from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from entities.schemas import AnomaliasOut, EstatisticasOut
from routes.dependencies import get_analise_controller, get_operador

router = APIRouter(prefix="/sensores", tags=["Análise de dados"])


@router.get("/{sensor_id}/estatisticas", response_model=EstatisticasOut)
def estatisticas(sensor_id: int, inicio: Optional[datetime] = None, fim: Optional[datetime] = None,
                 ctrl=Depends(get_analise_controller), operador=Depends(get_operador)):
    """Média, mínimo, máximo e desvio padrão, ignorando leituras SUSPEITA_RUIDO."""
    return ctrl.estatisticas(sensor_id, operador, inicio, fim)


@router.get("/{sensor_id}/anomalias", response_model=AnomaliasOut)
def anomalias(sensor_id: int, limiar: float = Query(3.0, gt=0),
              ctrl=Depends(get_analise_controller), operador=Depends(get_operador)):
    """Valores cujo z-score absoluto passa do limiar."""
    return ctrl.anomalias(sensor_id, operador, limiar)
