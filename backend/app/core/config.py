import logging
from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator
from functools import lru_cache

logger = logging.getLogger(__name__)


def _clean_url(v: str) -> str:
    """Quita espacios, comillas y barra final que pueden romper el cliente Supabase."""
    if not v:
        return ""
    s = v.strip().strip('"\'')
    return s.rstrip("/") if s.endswith("/") else s


class Settings(BaseSettings):
    # IA (centralizado en Google AI Studio / Gemini)
    google_api_key: str = ""  # Chat, documentos, alertas, embeddings RAG

    # Supabase (URL sin barra final: https://xxx.supabase.co)
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""  # JWT Secret from Project Settings > API

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_id_document: str = ""
    stripe_price_id_pro: str = ""

    # App
    frontend_url: str = "http://localhost:3000"
    environment: str = "development"

    # Resend (alertas por email)
    resend_api_key: str = ""
    resend_from_email: str = "alertas@tramitup.com"
    alerts_from_name: str = "Tramitup Alertas"

    # Performance settings
    max_chat_length: int = 2000
    rate_limit_free: int = 2
    rate_limit_pro: int = 100

    # External APIs timeouts
    google_ai_timeout: int = 30
    supabase_timeout: int = 10

    @field_validator("supabase_url", mode="before")
    @classmethod
    def clean_supabase_url(cls, v: str) -> str:
        return _clean_url(v) if isinstance(v, str) else v

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = ["development", "test", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v

    @model_validator(mode="after")
    def check_critical_keys(self) -> "Settings":
        """Detecta variables críticas vacías al arrancar y muestra errores claros."""
        missing: list[str] = []
        if not self.google_api_key:
            missing.append("GOOGLE_API_KEY (sin ella el chat no funcionará)")
        if not self.supabase_url:
            missing.append("SUPABASE_URL (sin ella no hay base de datos)")
        if not self.supabase_service_role_key:
            missing.append("SUPABASE_SERVICE_ROLE_KEY (sin ella no hay base de datos)")
        if not self.supabase_jwt_secret:
            missing.append("SUPABASE_JWT_SECRET (sin ella la autenticación fallará)")
        if self.is_production:
            if not self.stripe_secret_key:
                missing.append("STRIPE_SECRET_KEY (sin ella los pagos fallarán)")
            if not self.stripe_price_id_document:
                missing.append("STRIPE_PRICE_ID_DOCUMENT (sin ella el plan Document no se puede contratar)")
            if not self.stripe_price_id_pro:
                missing.append("STRIPE_PRICE_ID_PRO (sin ella el plan Pro no se puede contratar)")
            if self.frontend_url == "http://localhost:3000":
                missing.append("FRONTEND_URL (sigue con el valor por defecto localhost — CORS fallará en producción)")
        if missing:
            msg = "\n".join(f"  ❌ {m}" for m in missing)
            logger.warning(
                f"\n{'='*60}\n"
                f"⚠️  VARIABLES DE ENTORNO NO CONFIGURADAS:\n{msg}\n"
                f"{'='*60}"
            )
        return self

    @property
    def is_development(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    @property
    def is_test(self) -> bool:
        return self.environment == "test"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
