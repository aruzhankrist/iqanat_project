from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.structures.contracts.contracts import History
from app.helpers.jwt import get_current_user


app = APIRouter()


@app.get("/history")
def get_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(History).where(
        History.user_id == current_user["user_id"]  # type: ignore
    )

    events = db.execute(stmt).scalars().all()

    return events
