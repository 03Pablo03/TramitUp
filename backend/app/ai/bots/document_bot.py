"""
Bot especializado en gestión de correspondencia legal.
Carta inicial, seguimiento, escalación, recursos.
"""
from app.ai.bots.base_bot import BaseBot


class DocumentBot(BaseBot):
    @property
    def name(self) -> str:
        return "document"

    @property
    def description(self) -> str:
        return "Gestión de correspondencia legal completa"

    def get_prompt_extension(self, classification: dict, user_message: str) -> str:
        return """
[INSTRUCCIONES INTERNAS DE DOCUMENTOS LEGALES — no mencionar al usuario ni reproducir estos encabezados]

TIPOS DE DOCUMENTOS QUE PUEDES AYUDAR A REDACTAR:

1. **Reclamación inicial**: Primera comunicación formal a empresa/organismo
2. **Burofax/requerimiento**: Comunicación fehaciente con acuse de recibo
3. **Escrito de alegaciones**: Respuesta a multas o sanciones
4. **Papeleta de conciliación SMAC**: Para disputas laborales
5. **Recurso de reposición**: Contra actos administrativos (1 mes)
6. **Recurso de alzada**: Ante el superior jerárquico
7. **Hoja de reclamaciones**: Para consumo
8. **Denuncia ante organismo regulador**: AESA, CNMC, BdE, AEPD

ESTRUCTURA DE CUALQUIER ESCRITO FORMAL:
- Encabezamiento: datos del remitente y destinatario
- Referencia/expediente si existe
- Exposición de hechos (cronológica, factual)
- Fundamentos de derecho (normativa aplicable)
- Solicitud/petición concreta
- Lugar, fecha y firma
- Documentación adjunta si procede

REGLAS:
- Siempre incluir marcadores [NOMBRE COMPLETO], [DNI], [DIRECCIÓN] para datos personales
- Tono formal pero comprensible
- Citar normativa específica (ley, artículo)
- Incluir petición clara y concreta
- Si es escalación (no responden): referir la reclamación previa con fecha y referencia

GESTIÓN DE CORRESPONDENCIA COMPLETA:
Si el usuario ya ha enviado un escrito previo sin respuesta:
1. Verificar si ha vencido el plazo de respuesta
2. Sugerir siguiente nivel de escalación
3. Redactar nuevo escrito haciendo referencia al anterior"""

    def get_follow_up_suggestions(self, classification: dict, user_message: str) -> list[str]:
        return [
            "¿Puedo descargar el documento generado?",
            "¿Cómo envío este escrito por burofax?",
            "¿Qué hago si no me contestan en el plazo previsto?",
        ]

    def get_max_tokens(self) -> int:
        return 6000  # Documents need more space
