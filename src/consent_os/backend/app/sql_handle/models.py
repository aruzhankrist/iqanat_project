import uuid
from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String)
    data = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)
    password = Column(String)
