"""
Bot especializado en análisis de contratos.
Alquiler, laboral, hipotecas, seguros, suministros, compraventa.
"""
from app.ai.bots.base_bot import BaseBot


class ContractBot(BaseBot):
    @property
    def name(self) -> str:
        return "contract"

    @property
    def description(self) -> str:
        return "Análisis de contratos (alquiler, laboral, hipotecas, seguros)"

    def get_prompt_extension(self, classification: dict, user_message: str) -> str:
        return """
[INSTRUCCIONES INTERNAS DE ANÁLISIS DE CONTRATOS — no mencionar al usuario ni reproducir estos encabezados]

FLUJO OBLIGATORIO:

1. **IDENTIFICAR tipo de contrato**: Alquiler, laboral, hipoteca, seguro, suministro, compraventa.
2. **ANALIZAR cláusulas**: Revisar cada cláusula relevante contra la normativa.
3. **DETECTAR cláusulas abusivas**: Marcar CLARAMENTE las que sean abusivas según la ley.
4. **CLASIFICAR riesgo**: Para cada cláusula problemática: ALTO / MEDIO / BAJO.
5. **ACCIONES concretas**: Qué puede hacer el usuario para cada problema.

NORMATIVA POR TIPO DE CONTRATO:
- **Alquiler**: LAU 29/1994 (actualización IPC art.18, fianza art.36, duración mínima art.9-10, obras art.21-24)
- **Laboral**: Estatuto de los Trabajadores RDL 2/2015 (periodo prueba art.14, jornada art.34-38, despido art.49-56)
- **Hipoteca**: Ley 5/2019 de crédito inmobiliario (transparencia, gastos, cláusula suelo, IRPH)
- **Seguro**: Ley 50/1980 de Contrato de Seguro (deber info, exclusiones, siniestro)
- **Suministro**: Ley 24/2013 sector eléctrico, RD 1955/2000 (penalizaciones, cambio comercializadora)
- **Compraventa**: CC art.1445 ss, Ley 3/2014 consumidores (desistimiento 14 días)

CLÁUSULAS ABUSIVAS COMUNES (Ley 7/1998, arts. 82-91 TRLGDCU):
- Penalizaciones desproporcionadas
- Renuncias a derechos irrenunciables
- Períodos de permanencia excesivos sin justificación
- Cláusulas de sumisión a tribunales lejanos
- Modificaciones unilaterales del contrato
- Limitación de responsabilidad del profesional

FORMATO DE RESPUESTA:
Para cada cláusula problemática:
🔴/🟡/🔵 [RIESGO] **Título**
- Cláusula: "fragmento relevante"
- Problema: explicación clara
- Base legal: ley y artículo
- Acción: qué puede hacer el usuario"""

    def get_follow_up_suggestions(self, classification: dict, user_message: str) -> list[str]:
        return [
            "¿Puedo negarme a firmar estas cláusulas?",
            "¿Cómo renegocio las condiciones?",
            "¿Qué cláusulas son nulas de pleno derecho?",
        ]
