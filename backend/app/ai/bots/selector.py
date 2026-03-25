"""
Selector de bot especializado basado en clasificación y contexto del mensaje.
"""
import logging
from typing import Optional

from app.ai.bots.base_bot import BaseBot
from app.ai.bots.claims_bot import ClaimsBot
from app.ai.bots.contract_bot import ContractBot
from app.ai.bots.deadline_bot import DeadlineBot
from app.ai.bots.calculator_bot import CalculatorBot
from app.ai.bots.document_bot import DocumentBot

logger = logging.getLogger(__name__)

# Singleton instances
_BOTS: dict[str, BaseBot] = {
    "claims": ClaimsBot(),
    "contract": ContractBot(),
    "deadline": DeadlineBot(),
    "calculator": CalculatorBot(),
    "document": DocumentBot(),
}

# Category → bot mapping
_CATEGORY_BOT_MAP: dict[str, str] = {
    "consumo": "claims",
    "reclamaciones": "claims",
}

# Subcategory → bot mapping (takes priority over category)
_SUBCATEGORY_BOT_MAP: dict[str, str] = {
    "aerolinea": "claims",
    "banco": "claims",
    "telecom": "claims",
    "factura": "claims",
    "seguro": "claims",
    "suministro": "claims",
    "alquiler": "contract",
    "hipoteca": "contract",
    "contrato": "contract",
    "despido": "calculator",
    "finiquito": "calculator",
    "indemnizacion": "calculator",
    "pension": "calculator",
    "multa": "deadline",
}

# Keywords in the user message → bot override
_KEYWORD_BOT_MAP: list[tuple[list[str], str]] = [
    (["contrato", "cláusula", "firmar", "condiciones generales"], "contract"),
    (["calcular", "indemnización", "cuánto me corresponde", "cuánto dinero", "importe"], "calculator"),
    (["plazo", "plazos", "prescripción", "días hábiles", "fecha límite", "vencimiento"], "deadline"),
    (["carta", "escrito", "burofax", "reclamación formal", "alegaciones", "recurso", "papeleta"], "document"),
    (["reclamar", "reclamación", "cobro indebido", "devolver dinero"], "claims"),
]


def select_bot(classification: dict, user_message: str) -> Optional[BaseBot]:
    """
    Selecciona el bot más adecuado basándose en la clasificación y el mensaje.
    Returns None si no hay un bot especializado claro (usa prompt base).
    """
    message_lower = user_message.lower()
    category = classification.get("category", "")
    subcategory = classification.get("subcategory", "")

    # 1. Check keyword matches first (highest priority - user intent)
    for keywords, bot_name in _KEYWORD_BOT_MAP:
        if any(kw in message_lower for kw in keywords):
            bot = _BOTS.get(bot_name)
            if bot:
                logger.debug("Bot selected by keyword match: %s", bot_name)
                return bot

    # 2. Check subcategory mapping
    if subcategory:
        bot_name = _SUBCATEGORY_BOT_MAP.get(subcategory)
        if bot_name:
            bot = _BOTS.get(bot_name)
            if bot:
                logger.debug("Bot selected by subcategory '%s': %s", subcategory, bot_name)
                return bot

    # 3. Check category mapping
    if category:
        bot_name = _CATEGORY_BOT_MAP.get(category)
        if bot_name:
            bot = _BOTS.get(bot_name)
            if bot:
                logger.debug("Bot selected by category '%s': %s", category, bot_name)
                return bot

    # 4. No specialized bot - use base prompt
    logger.debug("No specialized bot selected, using base prompt")
    return None


def get_bot_by_name(name: str) -> Optional[BaseBot]:
    """Get a specific bot by name."""
    return _BOTS.get(name)
