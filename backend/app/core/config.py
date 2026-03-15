from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


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
