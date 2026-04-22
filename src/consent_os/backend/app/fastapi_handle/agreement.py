import datetime
import uuid
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.helpers.jwt import get_current_user
from app.sql_handle.models import ContractDB
from app.structures.contracts.contracts import (
    RiskLevel,
    Permissions,
)
from sqlalchemy import select

from app.structures.contracts.safety import (
    AgreementCreate,
    AgreementUpdate,
)


app = APIRouter()


@app.get("/agreements")
def get_user_agreements(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(ContractDB).where(ContractDB.user_id == current_user["user_id"])

    agreements = db.execute(stmt).scalars().all()

    return agreements


@app.get("/agreements/{agreement_id}")
def get_agreement(
    agreement_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(ContractDB).where(
        ContractDB.agreement_id == agreement_id  # type: ignore
    )

    agreement = db.execute(stmt).scalar_one_or_none()

    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")

    if agreement.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    return {
        "agreement_id": str(agreement.agreement_id),
        "title": agreement.title,
        "reason": agreement.reason,
        "content": agreement.content,
        "status": agreement.status,
        "risk_index": agreement.risk_index,
        "permissions": agreement.permissions,
        "metadata": agreement.metadata,
        "created": agreement.created,
    }


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


@app.post("/agreements/upload/analyse")
def analyse_agreement(
    agreement: bytes | str, reason: str, current_user=Depends(get_current_user)
):
    if not agreement:
        raise HTTPException(status_code=400, detail="Agreement text is required")

    # TODO:
    # здесь позже:
    # - вызов внешнего NLP/LLM сервиса
    # - анализ рисков
    # - извлечение permissions / metadata

    return {
        "success": True,
        "message": "Agreement analysis completed",
        "analysis": {
            "risk_index": "medium",
            "permissions": {
                "data_control": "high",
                "user_rights": "low",
                "transfer_of_rights_to_third_parties": "medium",
            },
            "metadata_flags": {"cookies": True, "tracking": True},
            "summary": (
                "Potential third-party data sharing and moderate privacy risk detected."
            ),
        },
    }


@app.patch("/agreements/{agreement_id}/update")
def update_agreement(
    agreement_id: str,
    update_info: AgreementUpdate,
    current_user=Depends(get_current_user),
):
    # TODO:
    # потом:
    # найти договор в БД
    # проверить ownership через JWT
    # обновить поля
    # поднять version +=1

    return {
        "success": True,
        "message": "Contract updated successfully",
        "agreement_id": agreement_id,
        "updated_fields": update_info.model_dump(exclude_none=True),
        "version": 2,
    }
