import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.hash import bcrypt


from app.helpers.password import verify_password
from app.structures.user.user import UserDB
from app.structures.user.login_request import LoginRequest
from app.structures.user.create_user import UserCreate
from app.helpers.jwt import create_access_token
from app.fastapi_handle.main import app, get_db


@app.get("/account")
def get_user_data(user_id, y):
    return user_id, y


@app.post("/login")
def get_login(user: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(UserDB).where(UserDB.email == user.email)  # type: ignore[]
    db_user = db.execute(stmt).scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({"user_id": db_user.user_id, "email": db_user.email})
    return {
        "token": token,
        "token_type": "bearer",
        "message": "login successful",
        "user_id": db_user.user_id,
    }


@app.post("/register")
def create_profile(user: UserCreate, db: Session = Depends(get_db)):
    data = {
        "user_id": uuid.uuid4(),
        "email": user.email,
        "password": bcrypt.hash(user.password),
    }
    new_user = UserDB(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "message": "регистрация прошла успешно"}
