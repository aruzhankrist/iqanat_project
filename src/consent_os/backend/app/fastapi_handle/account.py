import uuid
import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.helpers.password import verify_password
from app.structures.user.user import UserDB
from app.structures.user.login_request import LoginRequest
from app.structures.user.create_user import UserCreate
from app.helpers.jwt import create_access_token
from app.fastapi_handle.main import app, get_db
from app.helpers.password import hash_password
from app.structures.contracts.contracts import History, Agreements, RiskLevel


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
    # проверка существования
    stmt = select(UserDB).where(UserDB.email == user.email)  # type: ignore
    existing_user = db.execute(stmt).scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    risk_level = RiskLevel

    # создаём пользователя
    new_user = UserDB(
        user_id=uuid.uuid4(),  # можно убрать если default в модели
        email=user.email,
        username=user.username,
        password=hash_password(user.password),
        agreements=None,
        admin=False,
        history=None,
        privacy=RiskLevel(risk_level.low),
        notifycations=False,
        created=datetime.datetime.now(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "регистрация прошла успешно",
        "user_id": str(new_user.user_id),
    }
