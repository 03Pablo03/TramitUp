"""
Servicio de envío de emails con Resend para alertas de plazos.
"""
from datetime import date
from typing import Optional

from app.core.config import get_settings


def _format_date(d: date) -> str:
    """Formatea fecha en español."""
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{d.day} de {meses[d.month - 1]} de {d.year}"


def _urgency_class(days: int) -> tuple[str, str]:
    """(color_class, emoji) según días restantes."""
    if days <= 1:
        return "critical", "🔴"
    if days <= 3:
        return "urgent", "🟠"
    return "info", "🔵"


def send_deadline_alert(
    to_email: str,
    user_name: str,
    description: str,
    deadline_date: date,
    days_remaining: int,
    law_reference: str,
    alert_id: str,
) -> Optional[str]:
    """
    Envía email de alerta de plazo con Resend.
    Returns email_id para tracking, o None si falla.
    """
    try:
        import resend
    except ImportError:
        return None

    settings = get_settings()
    if not settings.resend_api_key:
        return None

    resend.api_key = settings.resend_api_key
    fecha_str = _format_date(deadline_date)
    _, emoji = _urgency_class(days_remaining)
    nombre = user_name or "Usuario"
    frontend = settings.frontend_url.rstrip("/")
    alerts_url = f"{frontend}/alerts"

    subject = f"⏰ Tu plazo vence en {days_remaining} días — {description[:50]}"

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alerta de plazo Tramitup</title>
</head>
<body style="margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f3f4f6;">
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
    <tr>
      <td style="padding: 24px 24px 16px; text-align: center;">
        <h1 style="margin: 0; font-size: 20px; color: #1e293b;">Tramitup</h1>
        <p style="margin: 4px 0 0; font-size: 12px; color: #64748b;">Entiende tus derechos</p>
      </td>
    </tr>
    <tr>
      <td style="padding: 0 24px 24px;">
        <div style="padding: 16px; border-radius: 8px; border-left: 4px solid {'#dc2626' if days_remaining <= 3 else '#f59e0b' if days_remaining <= 7 else '#2563eb'}; background: {'#fef2f2' if days_remaining <= 3 else '#fffbeb' if days_remaining <= 7 else '#eff6ff'};">
          <p style="margin: 0 0 8px; font-size: 14px; font-weight: 600; color: #1e293b;">{emoji} Alerta de plazo</p>
          <p style="margin: 0; font-size: 14px; color: #475569;">{description}</p>
        </div>
        <p style="margin: 20px 0 0; font-size: 15px; color: #334155; line-height: 1.6;">
          Hola {nombre},
        </p>
        <p style="margin: 12px 0 0; font-size: 15px; color: #334155; line-height: 1.6;">
          Te recordamos que el plazo para <strong>{description}</strong> vence el
          <strong>{fecha_str}</strong> ({days_remaining} días restantes).
        </p>
        <p style="margin: 12px 0 0; font-size: 13px; color: #64748b;">
          Referencia legal: {law_reference or "Normativa aplicable"}
        </p>
        <p style="margin: 20px 0 0; font-size: 14px; color: #64748b;">
          Si ya has resuelto este trámite, puedes descartar esta alerta desde tu panel.
        </p>
        <p style="margin: 24px 0 0; text-align: center;">
          <a href="{alerts_url}" style="display: inline-block; padding: 12px 24px; background: #1A56DB; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">Ver mis alertas →</a>
        </p>
      </td>
    </tr>
    <tr>
      <td style="padding: 16px 24px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8;">
        Tramitup ofrece información basada en normativa pública. No prestamos asesoramiento jurídico.
        <br><a href="{alerts_url}" style="color: #64748b;">Gestionar alertas</a>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    try:
        r = resend.Emails.send({
            "from": f"{settings.alerts_from_name} <{settings.resend_from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html,
        })
        return getattr(r, "id", None) or (r.get("id") if isinstance(r, dict) else None)
    except Exception:
        return None
