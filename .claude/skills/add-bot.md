Añade un nuevo bot especializado al sistema de bots de TramitUp.

**Pasos:**

1. Lee `backend/app/ai/bots/base_bot.py` para entender la clase base
2. Lee un bot existente (ej. `claims_bot.py`) como referencia de implementación
3. Crea `backend/app/ai/bots/{nombre}_bot.py` heredando de `BaseBot`:
   ```python
   from app.ai.bots.base_bot import BaseBot

   class NombreBot(BaseBot):
       name = "nombre_bot"
       description = "Descripción del bot"

       def can_handle(self, classification: dict, message: str) -> bool:
           # Retorna True si este bot debe manejar la consulta
           pass

       async def get_response(self, message: str, context: dict) -> AsyncGenerator:
           # Genera respuesta streaming
           pass
   ```
4. Añade el bot en `backend/app/ai/bots/selector.py`:
   - Importa la clase del bot
   - Añade al array `BOTS` en el orden correcto de prioridad
   - Define los criterios de selección en `select_bot()`
5. Añade el prompt del bot en `backend/app/ai/prompts/` si necesita uno especializado
6. Actualiza el agente `ai-specialist.md` con la descripción del nuevo bot

**Descripción del bot:** $ARGUMENTS
