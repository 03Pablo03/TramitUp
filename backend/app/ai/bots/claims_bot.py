"""
Bot especializado en reclamaciones de consumo.
Aerolíneas, bancos, telecom, suministros, seguros.
"""
from app.ai.bots.base_bot import BaseBot


class ClaimsBot(BaseBot):
    @property
    def name(self) -> str:
        return "claims"

    @property
    def description(self) -> str:
        return "Reclamaciones de consumo (aerolíneas, bancos, telecom, suministros)"

    def get_prompt_extension(self, classification: dict, user_message: str) -> str:
        subcategory = classification.get("subcategory", "")
        return f"""
[INSTRUCCIONES INTERNAS DE RECLAMACIONES — no mencionar al usuario ni reproducir estos encabezados]
Contexto de subcategoría para tu razonamiento interno: {subcategory}.

FLUJO OBLIGATORIO PARA RECLAMACIONES:

1. **IDENTIFICAR la empresa**: Pregunta el nombre exacto de la empresa si no lo ha dado.
2. **RECOPILAR hechos**: Pide los datos esenciales: qué pasó, cuándo, importe, referencia del contrato/factura.
3. **NORMATIVA aplicable**: Identifica y cita la normativa específica (ley, artículo, reglamento).
4. **CALCULAR importes**: Si aplica compensación o devolución, calcula el importe exacto.
5. **DATOS DE CONTACTO**: Incluye SIEMPRE el email/formulario de reclamaciones de la empresa (de la base de datos de contactos).
6. **GENERAR RECLAMACIÓN**: Ofrece generar un escrito formal de reclamación.

REGLAS ESPECIALES:
- Siempre distinguir entre: reclamación a la empresa → organismo regulador → juzgado
- Informar sobre plazos para cada nivel de escalación
- Si es reclamación bancaria: mencionar el SAC obligatorio (Circular 7/2013 BdE)
- Si es telecom: mencionar la Secretaría de Estado de Telecomunicaciones como vía alternativa
- Si es energía: mencionar la CNMC
- Si es seguro: mencionar el Defensor del Asegurado antes que la DGSFP

ESTRUCTURA DE RESPUESTA:
1. Resumen de la situación y derechos
2. Normativa aplicable con artículos
3. Pasos concretos con contactos directos
4. Plazos legales
5. Importes si aplica
6. Ofrecer documento/escrito"""

    def get_follow_up_suggestions(self, classification: dict, user_message: str) -> list[str]:
        return [
            "¿Cómo presento la reclamación por escrito?",
            "¿Qué hago si la empresa no me responde?",
            "¿Tengo derecho a pedir indemnización por daños?",
        ]
