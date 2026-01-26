# src/models/user.py
from datetime import datetime
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    sub: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="role", create_constraint=True),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    profile: Mapped["Profile"] = relationship(back_populates="user")

