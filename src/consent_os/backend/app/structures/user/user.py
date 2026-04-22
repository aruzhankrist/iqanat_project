import datetime
import uuid

from pydantic import BaseModel, EmailStr, Field
from app.structures.contracts.contracts import History, Agreements, RiskLevel


class UserDB(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    password: str | None = Field(max_length=128)
    username: str = Field(max_length=30)

    role: str = "user"

    privacy: RiskLevel
    notifycations: bool

    is_active: bool = True
    is_verified: bool = False

    last_login: datetime.datetime | None = None
    created: datetime.datetime
    deleted_at: datetime.datetime | None = None

    # security
    failed_login_attempts: int = 0
    locked_until: datetime.datetime | None = None

    # consent
    consent_version: str | None = None
    marketing_opt_in: bool = False

    # relations (логически, не как поле БД)
    agreements: Agreements | None
    history: History
