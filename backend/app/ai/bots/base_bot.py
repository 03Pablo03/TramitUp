"""
Interfaz base para bots especializados.
Cada bot extiende el prompt del sistema y post-procesa la respuesta.
"""
from abc import ABC, abstractmethod
from typing import Optional


class BaseBot(ABC):
    """Interfaz base para todos los bots especializados."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre interno del bot."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Descripción corta para logging/debug."""

    @abstractmethod
    def get_prompt_extension(self, classification: dict, user_message: str) -> str:
        """
        Devuelve texto adicional que se añade al system prompt base.
        Debe contener instrucciones especializadas del dominio del bot.
        """

    def get_follow_up_suggestions(self, classification: dict, user_message: str) -> list[str]:
        """Devuelve sugerencias de seguimiento específicas del dominio. Opcional."""
        return []

    def get_temperature(self) -> float:
        """Temperatura del LLM para este modo. Override si necesario."""
        return 0.3

    def get_max_tokens(self) -> int:
        """Max output tokens. Override si necesario."""
        return 4096
