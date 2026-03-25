"""
Calendario legal español.
Eventos legales recurrentes relevantes para ciudadanos.
"""
from datetime import date
from typing import List, Dict, Any

# Each event has: month, day (approx), title, description, category, url (optional)
LEGAL_CALENDAR_EVENTS = [
    # ── FISCAL ────────────────────────────────────────────────────────────
    {
        "month": 4, "day": 3,
        "title": "Apertura campaña de la Renta",
        "description": "Se abre el plazo para presentar la declaración de IRPF por internet.",
        "category": "fiscal",
        "duration_days": 90,  # Until June 30
    },
    {
        "month": 6, "day": 25,
        "title": "Último día Renta (presencial)",
        "description": "Último día para presentar la Renta presencialmente en oficinas de la AEAT.",
        "category": "fiscal",
    },
    {
        "month": 6, "day": 30,
        "title": "Fin campaña de la Renta",
        "description": "Fecha límite para presentar la declaración del IRPF.",
        "category": "fiscal",
    },
    {
        "month": 1, "day": 30,
        "title": "Modelo 303 IVA (4T)",
        "description": "Plazo para presentar la autoliquidación trimestral de IVA del 4º trimestre.",
        "category": "fiscal",
    },
    {
        "month": 7, "day": 25,
        "title": "Impuesto de Sociedades",
        "description": "Plazo para presentar el Impuesto de Sociedades (modelo 200).",
        "category": "fiscal",
    },
    # ── LABORAL ───────────────────────────────────────────────────────────
    {
        "month": 1, "day": 1,
        "title": "Actualización SMI",
        "description": "Entra en vigor el nuevo Salario Mínimo Interprofesional (si se aprueba).",
        "category": "laboral",
    },
    {
        "month": 1, "day": 15,
        "title": "Certificado de retenciones IRPF",
        "description": "Las empresas deben entregar el certificado de retenciones del año anterior.",
        "category": "laboral",
    },
    # ── VIVIENDA ──────────────────────────────────────────────────────────
    {
        "month": 1, "day": 1,
        "title": "Actualización IPC alquileres",
        "description": "Referencia para la actualización anual de rentas de alquiler según el INE.",
        "category": "vivienda",
    },
    {
        "month": 3, "day": 31,
        "title": "Certificado energético obligatorio",
        "description": "Recordatorio: para alquilar o vender un inmueble se necesita certificado energético vigente.",
        "category": "vivienda",
    },
    # ── TRÁFICO ───────────────────────────────────────────────────────────
    {
        "month": 1, "day": 1,
        "title": "Renovación permiso de conducir",
        "description": "Revisa la fecha de caducidad de tu carnet. Puedes renovarlo hasta 3 meses antes.",
        "category": "trafico",
    },
    {
        "month": 10, "day": 1,
        "title": "ITV vehículos",
        "description": "Revisa cuándo caduca tu ITV. Circular sin ITV vigente conlleva multa de hasta 500€.",
        "category": "trafico",
    },
    # ── CONSUMO ───────────────────────────────────────────────────────────
    {
        "month": 11, "day": 1,
        "title": "Black Friday / Compras navideñas",
        "description": "Recuerda: tienes 14 días de desistimiento en compras online (Ley 3/2014). Guarda facturas.",
        "category": "consumo",
    },
    {
        "month": 1, "day": 7,
        "title": "Rebajas de enero",
        "description": "Los productos rebajados tienen la misma garantía. Puedes devolver por defectos.",
        "category": "consumo",
    },
]


def get_upcoming_legal_events(
    from_date: date | None = None,
    days_ahead: int = 30,
    categories: list[str] | None = None,
) -> List[Dict[str, Any]]:
    """
    Devuelve eventos del calendario legal dentro de los próximos N días.
    Opcionalmente filtra por categorías.
    """
    today = from_date or date.today()
    results = []

    for event in LEGAL_CALENDAR_EVENTS:
        try:
            event_date = date(today.year, event["month"], event["day"])
        except ValueError:
            continue

        # If event has already passed this year, check next year
        if event_date < today:
            try:
                event_date = date(today.year + 1, event["month"], event["day"])
            except ValueError:
                continue

        days_until = (event_date - today).days
        if 0 <= days_until <= days_ahead:
            if categories and event.get("category") not in categories:
                continue

            results.append({
                "title": event["title"],
                "description": event["description"],
                "category": event.get("category", ""),
                "date": event_date.isoformat(),
                "days_until": days_until,
            })

    results.sort(key=lambda x: x["days_until"])
    return results
