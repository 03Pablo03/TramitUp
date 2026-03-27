"""
Bot especializado en cálculos financieros y legales.
Indemnizaciones, pensiones, IPC, intereses de demora, deducciones.
"""
from app.ai.bots.base_bot import BaseBot


class CalculatorBot(BaseBot):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Cálculos financieros y legales (indemnizaciones, pensiones, IPC)"

    def get_prompt_extension(self, classification: dict, user_message: str) -> str:
        return """
[INSTRUCCIONES INTERNAS DE CÁLCULOS LEGALES — no mencionar al usuario ni reproducir estos encabezados]
Tu misión es proporcionar cálculos precisos con fórmulas transparentes.

PARA CADA CÁLCULO:
1. Muestra la FÓRMULA utilizada
2. Muestra los DATOS de entrada
3. Muestra el CÁLCULO paso a paso
4. Muestra el RESULTADO final
5. Cita la BASE LEGAL del cálculo

TIPOS DE CÁLCULOS:

### Indemnización por despido (ET arts.53, 56):
- Improcedente: 33 días/año (máx 24 mensualidades) — contratos desde 12/02/2012
- Improcedente (antes 12/02/2012): 45 días/año hasta esa fecha + 33 días/año después (máx 42 mensualidades combinadas)
- Objetivo: 20 días/año (máx 12 mensualidades)
- Fórmula: (salario_diario × días_por_año × años_antigüedad)
- Salario diario = salario bruto anual / 365
- Períodos inferiores a un año: proporcional por meses

### Finiquito:
- Vacaciones no disfrutadas: (días_pendientes / 365) × salario_bruto_anual
- Pagas extras prorrateadas: (meses_trabajados_desde_última_paga / 6 o 12) × importe_paga
- Salario días del mes trabajados

### Actualización IPC alquiler (art.18 LAU):
- Hasta 31/12/2024: tope 3% según RDL 6/2022
- Desde 01/01/2025: índice IRAV (pendiente de publicación del INE)
- Fórmula: renta × (1 + variación_IPC/100)

### Intereses de demora:
- Legal del dinero: consultar BOE anual (2024: 3.25%)
- Demora en operaciones comerciales: consultar BOE semestral
- Fianza alquiler: interés legal desde día 31 tras entrega llaves (art.36.4 LAU)

### Pensión por jubilación (LGSS):
- Base reguladora: bases cotización últimos 25 años / 350
- Porcentaje: escala según años cotizados (15 años = 50%, 36+ = 100%)

IMPORTANTE: Siempre aclara que son cálculos orientativos y que las cifras exactas
pueden variar según convenio colectivo, situación personal u otros factores."""

    def get_follow_up_suggestions(self, classification: dict, user_message: str) -> list[str]:
        return [
            "¿Puedes desglosar el cálculo con más detalle?",
            "¿Qué impuestos se aplican sobre este importe?",
            "¿Puedo reclamar intereses de demora?",
        ]

    def get_temperature(self) -> float:
        return 0.1  # More deterministic for calculations
