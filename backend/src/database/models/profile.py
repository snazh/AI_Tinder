import enum
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Text, UniqueConstraint, CheckConstraint, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, utcnow
from enum import Enum as PyEnum


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

#
# class PersonalityType(enum.Enum):
#     INTROVERT = "introvert"
#     EXTROVERT = "extrovert"
#     AMBIVERT = "ambivert"
#
#
# class CommunicationStyle(enum.Enum):
#     DIRECT = "direct"
#     SOFT = "soft"
#     EMOTIONAL = "emotional"
#     LOGICAL = "logical"
#     PLAYFUL = "playful"
#
#
# class BodyType(PyEnum):
#     SLIM = "slim"
#     ATHLETIC = "athletic"
#     CURVY = "curvy"
#     PETITE = "petite"
#     PLUS_SIZE = "plus_size"
#
#
# class HairColor(PyEnum):
#     BLONDE = "blonde"
#     BRUNETTE = "brunette"
#     BLACK = "black"
#     RED = "red"
#     BROWN = "brown"
#     OTHER = "other"
#
#
# class Lifestyle(enum.Enum):
#     ACTIVE = "active"
#     HOME_LOVER = "home_lover"
#     PARTY_LOVER = "party_lover"
#     TRAVELER = "traveler"
#     CAREER_FOCUSED = "career_focused"
#
#
# class SoulmateType:
#     __tablename__ = "soulmate_type"
#     profile_id = Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
#     personality: Mapped[PersonalityType] = mapped_column(
#         Enum(PersonalityType, name="personality_type_enum", create_constraint=True),
#         nullable=False,
#         index=True,
#     )
#
#     body_type: Mapped[BodyType] = mapped_column(
#         Enum(BodyType, name="body_type_enum", create_constraint=True),
#         nullable=True,
#     )
#
#     lifestyle: Mapped[Lifestyle] = mapped_column(
#         Enum(Lifestyle, name="lifestyle_enum", create_constraint=True),
#         nullable=True,
#     )
#
#     communication_style: Mapped[CommunicationStyle] = mapped_column(
#         Enum(CommunicationStyle, name="communication_style_enum", create_constraint=True),
#         nullable=True,
#     )
