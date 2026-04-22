import uuid

from sqlalchemy import (
    UUID,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    JSON,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"

    # 🧾 identity
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    username = Column(String(30), nullable=False)

    # 👤 role system
    role = Column(String, default="user")

    # ⚖️ privacy / consent
    privacy = Column(String, nullable=False)
    notifycations = Column(Boolean, default=True)

    consent_version = Column(String, nullable=True)
    marketing_opt_in = Column(Boolean, default=False)

    # 🔐 status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # 🕒 activity tracking
    last_login = Column(DateTime, nullable=True)
    created = Column(DateTime, server_default=func.now())

    # 🔒 security
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # 📦 relations (ВАЖНО: это не поля, а связи)
    agreements = Column(JSON, nullable=True)
    history = Column(JSON, nullable=True)


class ContractDB(Base):
    __tablename__ = "contracts"

    # 🧾 идентификаторы
    agreement_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    # 📄 контент договора
    title = Column(String(30), nullable=False)
    reason = Column(String(30), nullable=False)
    content = Column(String(5000), nullable=False)

    # ⚖️ состояние договора
    active = Column(Boolean, default=True)
    status = Column(String, default="draft")  # draft / active / signed / revoked

    # 🔢 риск / версия
    risk_index = Column(String, nullable=False)
    version = Column(Integer, default=1)

    # 🔐 подпись
    is_signed = Column(Boolean, default=False)
    signed_at = Column(DateTime, nullable=True)

    # 🕒 время
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now(), nullable=True)

    # 🌐 контекст
    source_ip = Column(String, nullable=True)

    # 📦 сложные структуры (JSON поля)
    permissions = Column(JSON, nullable=False)
    browser_permissions = Column(JSON, nullable=True)
    metadata_info = Column(JSON, nullable=True)
    services = Column(JSON, nullable=True)
