import uuid

from sqlalchemy import (
    UUID,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import relationship
from datetime import datetime, timezone


Base = declarative_base()


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String)
    data = Column(String)


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)

    username = Column(String(30), nullable=False)

    notifycations = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    created = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # связи
    agreements = relationship("AgreementDB", back_populates="user")
    history = relationship("HistoryDB", back_populates="user")

    # если это enum/режимы
    privacy = Column(String)


class ContractDB(Base):
    __tablename__ = "contracts"

    agreement_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    title = Column(String(30), nullable=False)
    content = Column(Text, nullable=False)  # лучше Text, чем String(5000)
    reason = Column(String(30), nullable=False)

    active = Column(Boolean, default=True)

    created = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # если сложные структуры
    browser_permissions = Column(JSON, nullable=True)
    permissions = Column(JSON, nullable=False)
    metadata = Column(JSON, nullable=True)
    services = Column(JSON, nullable=True)

    # если это enum
    risk_index = Column(String)  # или Enum(...)

    # связь с пользователем
    user = relationship("UserDB", back_populates="agreements")
