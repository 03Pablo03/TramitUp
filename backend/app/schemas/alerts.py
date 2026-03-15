from datetime import date
from typing import Literal

from pydantic import BaseModel


class CreateAlertRequest(BaseModel):
    conversation_id: str | None = None
    description: str
    deadline_date: str  # YYYY-MM-DD
    law_reference: str | None = None
    notify_days_before: list[int] = [7, 3, 1]


class UpdateAlertRequest(BaseModel):
    status: Literal["active", "dismissed"] | None = None
    deadline_date: str | None = None  # YYYY-MM-DD


class AlertResponse(BaseModel):
    alert_id: str
    conversation_id: str | None
    description: str
    deadline_date: str
    law_reference: str | None
    days_remaining: int
    urgency: str
    status: str
    notifications_sent: list[str]
    created_at: str


class CreateAlertResponse(BaseModel):
    alert_id: str
    deadline_date: str
    notifications_scheduled: list[str]
