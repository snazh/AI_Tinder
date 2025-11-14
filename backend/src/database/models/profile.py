from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from enum import Enum as PyEnum



class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="profile")