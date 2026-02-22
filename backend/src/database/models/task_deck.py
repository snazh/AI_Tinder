from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Float, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, utcnow
from enum import Enum as PyEnum


class TaskStatus(PyEnum):
    open = "open"
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskCategory(Base):
    __tablename__ = "task_categories"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False
    )

    task: Mapped["Task"] = relationship(back_populates="task_links")
    category: Mapped["Category"] = relationship(back_populates="task_links")


class Category(Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    task_links: Mapped[list["TaskCategory"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status_enum", create_constraint=True),
        nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    performer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    task_links: Mapped[list["TaskCategory"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan"
    )
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id],
        back_populates="owned_tasks",
    )

    performer: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[performer_id],
        back_populates="performed_tasks",
    )
