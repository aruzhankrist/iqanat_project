from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.fastapi_handle.main import app, get_db
from consent_os.backend.app.helpers.jwt import get_current_user
from consent_os.backend.app.structures.contracts.contracts import ContractDB
from sqlalchemy import select


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


@app.delete("/agreements/{agreement_id}/delete")
def delete_agreement(
    agreement_id, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    stmt = select(ContractDB).where(
        ContractDB.agreement_id == agreement_id,
        ContractDB.user_id == current_user["user_id"],
    )
    agreement = db.execute(stmt).scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")

    db.delete(agreement)
    db.commit()
    return


@app.get("/agreements/upload/analyse")
def analyse_agreement(agreement: bytes | str, reason: str):
    return agreement


@app.get("/contract")
def get_text(user_id: str, infomation: str):
    return "contract added"
