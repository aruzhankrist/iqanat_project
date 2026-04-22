from pydantic import BaseModel
from app.structures.contracts.contracts import RiskLevel


class AccountSettingsUpdate(BaseModel):
    username: str | None = None

    privacy: RiskLevel | None = None

    notifications: bool | None = None

    marketing_opt_in: bool | None = None
