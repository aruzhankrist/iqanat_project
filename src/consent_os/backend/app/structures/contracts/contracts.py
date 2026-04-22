import datetime
import uuid

from pydantic import BaseModel, Field
from enum import Enum


class Metadata(BaseModel):
    # 🍪 cookies / storage
    cookies: bool = True
    tracking_cookies: bool = False
    session_storage: bool = True
    local_storage: bool = False

    # 🧠 device info
    device_data: bool = True
    device_id: str | None = None
    device_type: str | None = None  # mobile / desktop / tablet
    os: str | None = None
    os_version: str | None = None

    # 🌐 browser info
    browser_data: bool = True
    browser_name: str | None = None
    browser_version: str | None = None
    user_agent: str | None = None

    # 📍 network / location
    ip_address: str | None = None
    geo_location: str | None = None
    timezone: str | None = None
    language: str | None = None

    # 📊 analytics / behavior
    page_views: bool = True
    click_tracking: bool = False
    scroll_tracking: bool = False
    session_duration_tracking: bool = True
    event_tracking: bool = False

    # 🔐 security signals
    login_attempt_tracking: bool = True
    anomaly_detection: bool = True
    fraud_detection: bool = False

    # 🧾 consent metadata
    consent_version: str | None = None
    consent_timestamp: str | None = None
    consent_ip: str | None = None
    consent_device_fingerprint: str | None = None

    # ⚙️ system
    debug_mode: bool = False


class BrowserPermissions(BaseModel):
    # 📍 location
    geolocation: bool = False

    # 🎥 media
    camera: bool = False
    microphone: bool = False
    screen_capture: bool = False

    # 🔔 notifications
    notifications: bool = False
    push_notifications: bool = False

    # 💾 storage
    clipboard_read: bool = False
    clipboard_write: bool = False
    local_storage: bool = True
    session_storage: bool = True

    # 🔐 device / sensors
    device_orientation: bool = False
    device_motion: bool = False

    # 🌐 network / system
    background_sync: bool = False
    downloads: bool = True

    # 🧠 advanced / tracking
    cookies: bool = True
    third_party_cookies: bool = False
    fingerprinting_protection: bool = False

    # 🔊 media playback
    autoplay_media: bool = True


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Permissions(BaseModel):
    # юридические
    changing_rules: RiskLevel
    disclaimer: RiskLevel
    transfer_of_rights_to_third_parties: RiskLevel
    user_rights: RiskLevel
    consent_data: RiskLevel

    # данные пользователя
    data_control: RiskLevel
    gathering_documents: RiskLevel
    uploaded_data: RiskLevel
    transaction_data: RiskLevel

    # системные данные
    technical_specifications: RiskLevel
    behavioral_data: RiskLevel

    # дополнительные поля
    risk_index: RiskLevel | None = None


class Services(BaseModel):
    name: str = Field(max_length=30)


class ContractDB(BaseModel):
    content: str = Field(max_length=5_000)
    browser_permissions: BrowserPermissions | None
    permissions: Permissions
    risk_index: RiskLevel
    user_id: uuid.UUID
    agreement_id: uuid.UUID
    title: str = Field(max_length=30)
    active: bool
    created: datetime.datetime
    metadata: Metadata | None
    reason: str = Field(max_length=30)
    services: Services | None


class Agreements(BaseModel):
    contract_id: str
    user_id: str
    reason: str = Field(max_length=30)
    services: Services


class History(BaseModel):
    contracts: ContractDB
    user_id: str
