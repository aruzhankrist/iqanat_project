import datetime
import uuid

from pydantic import BaseModel, Field
from enum import Enum


class Metadata(BaseModel):
    cookies: bool
    device_data: bool
    browser_data: bool


class BrowserPermissions(BaseModel):
    geoposition: bool
    camera: bool
    microphone: bool


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Modes(BaseModel):
    level: RiskLevel


class Permissions(BaseModel):
    changing_rules: Modes
    disclaimer: Modes
    transfer_of_rights_to_third_parties: Modes
    data_control: Modes
    gathering_documents: Modes
    user_rights: Modes


class ContractDB(BaseModel):
    text: str = Field(max_length=5_000)
    browser_permissions: BrowserPermissions
    permissions: Permissions
    risk_index: Modes
    user_id: uuid.UUID
    agreement_id: str
    service: str = Field(max_length=30)
    active: bool
    access_to_contract: str
    created: datetime.datetime
    metadata: Metadata


class Services(BaseModel):
    name: str = Field(max_length=30)


class Agreements(BaseModel):
    contract_id: str
    user_id: str
    reason: str = Field(max_length=30)
    services: Services


class History(BaseModel):
    contracts: ContractDB
    user_id: str
