import datetime
import uuid

from pydantic import BaseModel, EmailStr, Field
from app.structures.contracts.contracts import History, Agreements, RiskLevel


class UserDB(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    password: str = Field(max_length=128)
    agreements: Agreements
    history: History
    username: str = Field(max_length=30)
    privacy: RiskLevel
    notifycations: bool
    admin: bool
    created: datetime.datetime
