import uuid

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.hash import bcrypt


from app.helpers.password import verify_password
from app.sql_handle.database import SessionLocal
from app.structures.user import UserCreate, UserDB, LoginRequest


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/contract")
def get_text(user_id: str, infomation: str):
    return "contract added"


@app.get("/agreements")
def get_user_agreements(user_id: str):
    return None


@app.get("/agreements/{agreement_id}")
def get_agreement(user_id: str, agreement_id: str):
    return agreement_id


@app.get("/agreements/upload")
def get_uploaded_agreement(
    user_id: str, agreement: bytes | str, reason: str, title: str
):
    return agreement


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

    return {"success": True, "message": "login successful", "user_id": db_user.user_id}


@app.get("/settings")
def get_settings(user_id: str):
    return


@app.get("/history")
def get_history(user_id):
    return


@app.delete("/agreements/{agreement_id}/delete")
def delete_agreement(user_id):
    return


@app.get("/agreements/upload/analyse")
def analyse_agreement(agreement: bytes | str, reason: str):
    return agreement


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
