"""
Calculadora de indemnizaciones laborales españolas.

Fórmulas según:
- Despido improcedente: ET art.56 + Ley 3/2012 Disp. Transitoria 5ª
- Despido procedente/objetivo: ET art.53
- Fin de contrato temporal: ET art.49.1.c

La fecha de reforma laboral (12 feb 2012) divide el cálculo para contratos
anteriores a esa fecha en dos tramos con distintos multiplicadores.
"""
from datetime import date
from dataclasses import dataclass, field

# Ley 3/2012, en vigor desde el 12 de febrero de 2012
REFORMA_LABORAL = date(2012, 2, 12)


@dataclass
class TramoCalculo:
    desde: str
    hasta: str
    dias_trabajados: int
    anios: float
    dias_indemnizacion: float
    importe: float
    nota: str


@dataclass
class ResultadoCalculo:
    tipo: str
    importe_total: float
    salario_diario: float
    tramos: list[TramoCalculo] = field(default_factory=list)
    base_legal: str = ""
    nota_orientativa: str = ""


def _salario_diario(salario_anual: float) -> float:
    return salario_anual / 365


def _anios(inicio: date, fin: date) -> float:
    return max(0.0, (fin - inicio).days / 365)


def calcular(
    tipo: str,
    salario_anual_bruto: float,
    fecha_inicio: date,
    fecha_fin: date,
) -> ResultadoCalculo:
    """
    Punto de entrada único. tipo puede ser:
      'despido_improcedente' | 'despido_procedente' | 'fin_contrato_temporal'
    """
    if tipo == "despido_improcedente":
        return _despido_improcedente(salario_anual_bruto, fecha_inicio, fecha_fin)
    elif tipo == "despido_procedente":
        return _despido_procedente(salario_anual_bruto, fecha_inicio, fecha_fin)
    elif tipo == "fin_contrato_temporal":
        return _fin_contrato_temporal(salario_anual_bruto, fecha_inicio, fecha_fin)
    else:
        raise ValueError(f"Tipo de cálculo desconocido: {tipo}")


# ─────────────────────────────────────────────────────────────────────────────
# Despido improcedente — ET art.56 + Ley 3/2012 DT 5ª
# ─────────────────────────────────────────────────────────────────────────────

def _despido_improcedente(
    salario_anual: float,
    fecha_inicio: date,
    fecha_fin: date,
) -> ResultadoCalculo:
    sd = _salario_diario(salario_anual)
    tramos: list[TramoCalculo] = []

    if fecha_inicio >= REFORMA_LABORAL:
        # ── Contrato 100% post-reforma ────────────────────────────────────────
        anios = _anios(fecha_inicio, fecha_fin)
        dias_ind = anios * 33
        dias_ind = min(dias_ind, 720)          # máx 24 mensualidades ≈ 720 días
        importe = round(dias_ind * sd, 2)

        tramos.append(TramoCalculo(
            desde=fecha_inicio.isoformat(),
            hasta=fecha_fin.isoformat(),
            dias_trabajados=(fecha_fin - fecha_inicio).days,
            anios=round(anios, 2),
            dias_indemnizacion=round(dias_ind, 2),
            importe=importe,
            nota="33 días por año (Ley 3/2012)",
        ))
        total = importe

    else:
        # ── Contrato mixto: tramo pre + post reforma ──────────────────────────
        # Tramo 1: inicio → 11 feb 2012  (45 días/año, máx 42 mensualidades)
        fin1 = min(fecha_fin, date(2012, 2, 11))
        anios1 = _anios(fecha_inicio, fin1)
        dias_ind1_raw = anios1 * 45
        dias_ind1 = min(dias_ind1_raw, 1260)   # máx 42 mensualidades

        tramos.append(TramoCalculo(
            desde=fecha_inicio.isoformat(),
            hasta=fin1.isoformat(),
            dias_trabajados=(fin1 - fecha_inicio).days,
            anios=round(anios1, 2),
            dias_indemnizacion=round(dias_ind1, 2),
            importe=round(dias_ind1 * sd, 2),
            nota="45 días por año (contrato anterior al 12 feb 2012)",
        ))

        dias_ind2 = 0.0
        if fecha_fin > REFORMA_LABORAL:
            # Tramo 2: 12 feb 2012 → fecha_fin  (33 días/año)
            inicio2 = REFORMA_LABORAL
            anios2 = _anios(inicio2, fecha_fin)
            dias_ind2 = anios2 * 33

            tramos.append(TramoCalculo(
                desde=inicio2.isoformat(),
                hasta=fecha_fin.isoformat(),
                dias_trabajados=(fecha_fin - inicio2).days,
                anios=round(anios2, 2),
                dias_indemnizacion=round(dias_ind2, 2),
                importe=round(dias_ind2 * sd, 2),
                nota="33 días por año (Ley 3/2012)",
            ))

        # Límite total según DT 5ª Ley 3/2012:
        # No puede superar 720 días, SALVO que el tramo 1 sin cap ya los supere.
        # En ningún caso puede superar 42 mensualidades (1260 días).
        tope = max(720.0, dias_ind1_raw)
        tope = min(tope, 1260.0)
        total_dias = min(dias_ind1 + dias_ind2, tope)
        total = round(total_dias * sd, 2)

    return ResultadoCalculo(
        tipo="despido_improcedente",
        importe_total=total,
        salario_diario=round(sd, 2),
        tramos=tramos,
        base_legal="ET art. 56 y Ley 3/2012, Disp. Transitoria 5.ª",
        nota_orientativa=(
            "Cálculo orientativo basado en salario fijo anual. El importe real puede variar "
            "si existen variables, comisiones, complementos salariales o pagas adicionales. "
            "Consulta con un especialista laboral para confirmar el importe exacto."
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Despido procedente / por causas objetivas — ET art.53
# ─────────────────────────────────────────────────────────────────────────────

def _despido_procedente(
    salario_anual: float,
    fecha_inicio: date,
    fecha_fin: date,
) -> ResultadoCalculo:
    sd = _salario_diario(salario_anual)
    anios = _anios(fecha_inicio, fecha_fin)
    dias_ind = anios * 20
    dias_ind = min(dias_ind, 360)              # máx 12 mensualidades ≈ 360 días
    importe = round(dias_ind * sd, 2)

    return ResultadoCalculo(
        tipo="despido_procedente",
        importe_total=importe,
        salario_diario=round(sd, 2),
        tramos=[TramoCalculo(
            desde=fecha_inicio.isoformat(),
            hasta=fecha_fin.isoformat(),
            dias_trabajados=(fecha_fin - fecha_inicio).days,
            anios=round(anios, 2),
            dias_indemnizacion=round(dias_ind, 2),
            importe=importe,
            nota="20 días por año (causas objetivas)",
        )],
        base_legal="ET art. 53.1.b",
        nota_orientativa=(
            "Aplica a despidos por causas económicas, técnicas, organizativas o de producción. "
            "Si la empresa no cumple los requisitos formales, el despido puede declararse improcedente "
            "y correspondería una indemnización mayor (33 días/año)."
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Fin de contrato temporal — ET art.49.1.c
# ─────────────────────────────────────────────────────────────────────────────

def _fin_contrato_temporal(
    salario_anual: float,
    fecha_inicio: date,
    fecha_fin: date,
) -> ResultadoCalculo:
    sd = _salario_diario(salario_anual)
    anios = _anios(fecha_inicio, fecha_fin)
    # 12 días/año para contratos temporales (desde 2015 para obra/servicio y eventualidad)
    dias_ind = anios * 12
    importe = round(dias_ind * sd, 2)

    return ResultadoCalculo(
        tipo="fin_contrato_temporal",
        importe_total=importe,
        salario_diario=round(sd, 2),
        tramos=[TramoCalculo(
            desde=fecha_inicio.isoformat(),
            hasta=fecha_fin.isoformat(),
            dias_trabajados=(fecha_fin - fecha_inicio).days,
            anios=round(anios, 2),
            dias_indemnizacion=round(dias_ind, 2),
            importe=importe,
            nota="12 días por año (contratos temporales)",
        )],
        base_legal="ET art. 49.1.c",
        nota_orientativa=(
            "Aplica a contratos por obra, eventualidad o interinidad al extinguirse por causa pactada. "
            "No aplica si el contrato se convierte en indefinido o si la extinción es por baja voluntaria."
        ),
    )
