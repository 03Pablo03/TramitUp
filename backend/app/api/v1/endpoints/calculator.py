from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator

from app.core.auth import require_auth
from app.services.compensation_calculator import calcular, TramoCalculo

router = APIRouter()


class CalculatorRequest(BaseModel):
    tipo: str
    salario_anual_bruto: float
    fecha_inicio: date
    fecha_fin: date

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        opciones = {"despido_improcedente", "despido_procedente", "fin_contrato_temporal"}
        if v not in opciones:
            raise ValueError(f"tipo debe ser uno de: {opciones}")
        return v

    @field_validator("salario_anual_bruto")
    @classmethod
    def salario_positivo(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El salario debe ser mayor que 0")
        return v

    @field_validator("fecha_fin")
    @classmethod
    def fechas_coherentes(cls, v: date, info) -> date:
        inicio = info.data.get("fecha_inicio")
        if inicio and v <= inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


class TramoResponse(BaseModel):
    desde: str
    hasta: str
    dias_trabajados: int
    anios: float
    dias_indemnizacion: float
    importe: float
    nota: str


class CalculatorResponse(BaseModel):
    tipo: str
    importe_total: float
    salario_diario: float
    tramos: list[TramoResponse]
    base_legal: str
    nota_orientativa: str


@router.post("", response_model=CalculatorResponse)
def calcular_indemnizacion(
    request: CalculatorRequest,
    _user_id: str = Depends(require_auth),
):
    """
    Calcula la indemnización laboral según el tipo de extinción de contrato.
    Requiere autenticación.
    """
    try:
        resultado = calcular(
            tipo=request.tipo,
            salario_anual_bruto=request.salario_anual_bruto,
            fecha_inicio=request.fecha_inicio,
            fecha_fin=request.fecha_fin,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CalculatorResponse(
        tipo=resultado.tipo,
        importe_total=resultado.importe_total,
        salario_diario=resultado.salario_diario,
        tramos=[
            TramoResponse(
                desde=t.desde,
                hasta=t.hasta,
                dias_trabajados=t.dias_trabajados,
                anios=t.anios,
                dias_indemnizacion=t.dias_indemnizacion,
                importe=t.importe,
                nota=t.nota,
            )
            for t in resultado.tramos
        ],
        base_legal=resultado.base_legal,
        nota_orientativa=resultado.nota_orientativa,
    )
