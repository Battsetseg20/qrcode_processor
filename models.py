import uuid
from datetime import datetime

from database import Base  # Import Base from database module
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


"""
All the models (tables) for the database.
"""


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    department_roles = relationship("DepartmentRole", back_populates="user")


class Department(Base):
    __tablename__ = "departments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class DepartmentRole(Base):
    __tablename__ = "user_department_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="department_roles")

    department_id = Column(
        UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="CASCADE"),
        primary_key=True,
    )
    department = relationship("Department")

    role = Column(Enum("member", "admin", name="role"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
