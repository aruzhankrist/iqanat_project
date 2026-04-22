from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.helpers.jwt import get_current_user
from app.structures.user.user import UserDB
from sqlalchemy.orm import Session


app = APIRouter()


@app.get("/settings")
def get_settings(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(UserDB).where(UserDB.user_id == current_user["user_id"])

    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "privacy": user.privacy,
        "notifications": user.notifications,
        "marketing_opt_in": user.marketing_opt_in,
        "role": user.role,
    }
