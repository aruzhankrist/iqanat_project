import uuid
import datetime

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.helpers.password import verify_password
from app.structures.user.user import UserDB
from app.structures.user.login_request import LoginRequest
from app.structures.user.create_user import UserCreate
from app.structures.user.user_update import AccountSettingsUpdate
from app.helpers.jwt import create_access_token
from app.db.session import get_db
from app.helpers.password import hash_password
from app.structures.contracts.contracts import History, RiskLevel
from app.helpers.jwt import get_current_user


app = APIRouter()


@app.get("/account")
def get_user_data(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(UserDB).where(UserDB.user_id == current_user["user_id"])

    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": str(user.user_id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "privacy": user.privacy,
        "notifications": user.notifycations,
        "is_verified": user.is_verified,
        "created": user.created,
        "last_login": user.last_login,
    }


@app.patch("/account/settings")
def change_settings(
    settings: AccountSettingsUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(UserDB).where(UserDB.user_id == current_user["user_id"])

    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = settings.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "settings updated",
        "updated_fields": list(data.keys()),
    }


@app.delete("/account/delete")
def delete_user_data(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(UserDB).where(UserDB.user_id == current_user["user_id"])

    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = None
    user.email = f"deleted_{user.user_id}@none.org"
    user.username = "deleted_user"
    user.is_active = False
    user.deleted_at = datetime.datetime.now(datetime.timezone.utc)

    db.add(user)
    db.commit()

    return {"success": True, "message": "account deactivated"}


@app.post("/login")
def get_login(user: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(UserDB).where(UserDB.email == user.email)  # type: ignore[]
    db_user = db.execute(stmt).scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.password:
        raise HTTPException(status_code=400, detail="User has no password set")

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
    stmt = select(UserDB).where(UserDB.email == user.email)  # type: ignore
    existing_user = db.execute(stmt).scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user_id = uuid.uuid4()
    history_entry = History(
        nickname=user.username,
        action="user_registered",
        contract_id=None,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        contract_snapshot=None,
    )

    new_user = UserDB(
        user_id=new_user_id,
        email=user.email,
        username=user.username,
        password=hash_password(user.password),
        role="user",
        privacy=RiskLevel.low,
        notifycations=False,
        is_active=True,
        is_verified=False,
        failed_login_attempts=0,
        agreements=None,
        history=[history_entry],
        created=datetime.datetime.now(datetime.timezone.utc),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "регистрация прошла успешно",
        "user_id": str(new_user.user_id),
    }
