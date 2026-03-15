"""
Proxy de login. El onboarding se completa via API Next.js (cookies).
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.supabase_client import get_supabase_client

router = APIRouter()


class SignInRequest(BaseModel):
    email: str
    password: str


@router.post("/signin")
async def signin_proxy(req: SignInRequest):
    """Proxy de login: el backend llama a Supabase y devuelve los tokens."""
    try:
        supabase = get_supabase_client()
        resp = supabase.auth.sign_in_with_password({"email": req.email, "password": req.password})
        if not resp.session:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        return {
            "access_token": resp.session.access_token,
            "refresh_token": resp.session.refresh_token,
            "expires_in": resp.session.expires_in,
            "expires_at": resp.session.expires_at,
        }
    except Exception as e:
        msg = str(e).lower()
        if "invalid" in msg or "credentials" in msg or "email" in msg:
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
        raise HTTPException(status_code=502, detail=f"Error de conexión con Supabase: {e}")
