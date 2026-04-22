from fastapi import UploadFile
from pydantic import BaseModel, Field

from app.structures.contracts.contracts import RiskLevel


class AgreementCreate(BaseModel):
    title: str = Field(max_length=30)
    reason: str = Field(max_length=30)
    file: UploadFile = Field(max_length=5_000)
    risk_level: RiskLevel


class AgreementUpdate(BaseModel):
    title: str | None = None
    reason: str | None = None
    content: str | None = None
