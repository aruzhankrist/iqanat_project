from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(max_length=30)
    email: EmailStr
    password: str = Field(max_length=128)
