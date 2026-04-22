import datetime
import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.fastapi_handle.main import app, get_db
from consent_os.backend.app.helpers.jwt import get_current_user
from consent_os.backend.app.structures.contracts.contracts import (
    ContractDB,
    RiskLevel,
    Permissions,
)
from sqlalchemy import select

from consent_os.backend.app.structures.contracts.safety import AgreementCreate


@app.get("/agreements")
def get_user_agreements(user_id: str):
    return None


@app.get("/agreements/{agreement_id}")
def get_agreement(agreement_id: str):
    return agreement_id


@app.post("/agreements/upload")
def upload_agreement(
    data: AgreementCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    content: str = str(data.file.read())
    risk = RiskLevel(data.risk_level)

    permissions = Permissions(
        changing_rules=RiskLevel.low,
        disclaimer=RiskLevel.low,
        transfer_of_rights_to_third_parties=RiskLevel.medium,
        data_control=RiskLevel.high,
        gathering_documents=RiskLevel.medium,
        user_rights=RiskLevel.high,
        technical_specifications=RiskLevel.low,
        behavioral_data=RiskLevel.medium,
        consent_data=RiskLevel.high,
        transaction_data=RiskLevel.medium,
        uploaded_data=RiskLevel.high,
        risk_index=risk,
    )

    new_agreement = ContractDB(
        title=data.title,
        reason=data.reason,
        content=content,
        user_id=current_user["user_id"],
        agreement_id=uuid.uuid4(),
        permissions=permissions,
        risk_index=risk,
        browser_permissions=None,
        active=True,
        created=datetime.datetime.now(),
        metadata=None,
        services=None,
    )

    db.add(new_agreement)
    db.commit()

    return {"message": "uploaded"}


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


@app.get("/agreements/{agreement_id}/update")
def get_text(agreement_id: str, update_info):
    return "contract upd"
