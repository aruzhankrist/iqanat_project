import datetime

from pydantic import BaseModel, EmailStr, Field
from app.structures.contracts import History, Agreements, Modes


class UserDB(BaseModel):
    user_id: str
    email: EmailStr
    password: str = Field(max_length=128)
    agreements: Agreements
    history: History
    username: str = Field(max_length=30)
    privacy: Modes
    notifycations: bool
    admin: bool
    created: datetime.datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128)


class UserCreate(BaseModel):
    username: str = Field(max_length=30)
    email: EmailStr
    password: str = Field(max_length=128)


class UserResponse(BaseModel):
    id: str
    username: str
