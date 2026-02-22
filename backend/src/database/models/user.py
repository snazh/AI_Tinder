# src/models/user.py
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, utcnow
from enum import Enum as PyEnum


class UserRole(PyEnum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    sub: Mapped[str] = mapped_column(String(255), unique=True, nullable=False,index=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="role", create_constraint=True),
        nullable=False,index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow,
                                                 nullable=False)

    telegram_chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")

    owned_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        foreign_keys="Task.owner_id",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    performed_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        foreign_keys="Task.performer_id",
        back_populates="performer",
    )