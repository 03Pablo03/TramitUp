from pydantic import BaseModel


class UserProfile(BaseModel):
    id: str
    email: str | None
    plan: str  # free | document | pro
    documents_used_today: int
    remaining_chats_today: int  # -1 = unlimited
