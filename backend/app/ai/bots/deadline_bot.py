"""
Bot especializado en identificación exhaustiva de plazos legales.
"""
from app.ai.bots.base_bot import BaseBot


class DeadlineBot(BaseBot):
    @property
    def name(self) -> str:
        return "deadline"

    @property
    def description(self) -> str:
        return "Identificación exhaustiva de plazos legales"

    def get_prompt_extension(self, classification: dict, user_message: str) -> str:
        return """
[INSTRUCCIONES INTERNAS DE PLAZOS LEGALES — no mencionar al usuario ni reproducir estos encabezados]
Tu misión es identificar TODOS los plazos que afectan al usuario.

IDENTIFICA EXHAUSTIVAMENTE:

1. **Plazo principal**: El más urgente o relevante para el caso.
2. **Plazos derivados**: Otros plazos que se activan según la acción del usuario.
3. **Plazo de prescripción**: Cuándo caduca el derecho a reclamar.
4. **Plazo de respuesta de la contraparte**: Cuánto debe esperar el usuario.
5. **Plazos administrativos**: Si hay que presentar algo ante un organismo.

PARA CADA PLAZO, INCLUYE:
- Descripción clara de qué plazo es
- Número de días (hábiles o naturales — especificar)
- Fecha de referencia (desde cuándo se cuenta)
- Referencia normativa exacta (ley, artículo)
- Nivel de urgencia: CRÍTICO / IMPORTANTE / INFORMATIVO
- Consecuencia de incumplir el plazo

PLAZOS FRECUENTES POR CATEGORÍA:
- **Despido**: 20 días hábiles papeleta SMAC (art.59.3 ET), 15 días hábiles pedir paro SEPE
- **Multa tráfico**: 20 días naturales alegaciones, 1 mes recurso reposición, 2 meses contencioso
- **Consumo**: 30 días respuesta empresa, 1 año prescripción general (art.123 TRLGDCU)
- **Alquiler/fianza**: 30 días devolución fianza (art.36.4 LAU), 5 años prescripción
- **Hacienda**: 10/15/20 días según tipo, 1 mes recurso reposición, 2 meses contencioso
- **Vuelos**: 1 mes respuesta aerolínea, 1 año prescripción judicial (art.35 Ley 48/1960)

FORMATO: Lista cada plazo de forma clara y estructurada para que el sistema
pueda detectarlos automáticamente y ofrecer alertas al usuario."""

    def get_follow_up_suggestions(self, classification: dict, user_message: str) -> list[str]:
        return [
            "¿Cómo puedo activar alertas para estos plazos?",
            "¿Qué consecuencias tiene que se me pase el plazo?",
            "¿Existe alguna forma de interrumpir o suspender el plazo?",
        ]
