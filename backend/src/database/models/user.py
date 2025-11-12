# src/models/user.py
from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    admin = "admin"
    user = "user"



class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="role", create_constraint=True),
        nullable=False,
        default=UserRole.user
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

#
# class UserAnketa(Base):
#     pass