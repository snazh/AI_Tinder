from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Text, UniqueConstraint, CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, utcnow


class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False,
                                         index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    avatar_path: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped["User"] = relationship(back_populates="profile")

    likes_sent: Mapped[list["Like"]] = relationship(
        foreign_keys="Like.liker_id",
        back_populates="liker",
        cascade="all, delete-orphan"
    )

    likes_received: Mapped[list["Like"]] = relationship(
        foreign_keys="Like.liked_id",
        back_populates="liked",
        cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow,
                                                 nullable=False)


class Like(Base):
    __tablename__ = "likes"
    liker_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


    liker: Mapped["Profile"] = relationship(
        foreign_keys=[liker_id],
        back_populates="likes_sent"
    )
    liked: Mapped["Profile"] = relationship(
        foreign_keys=[liked_id],
        back_populates="likes_received"
    )
    __table_args__ = (
        UniqueConstraint("liker_id", "liked_id", name="unique_like"),
        CheckConstraint("liker_id <> liked_id", name="liker_not_equal_liked"),
    )
