from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileCreateSchema(BaseModel):
    username: str
    avatar_path: str
    user_id: int
    age: int
    description: str
    model_config = ConfigDict(from_attributes=True)


class ProfileUpdateSchema(BaseModel):
    username: Optional[str] = None
    avatar_path: Optional[str] = None
    age: Optional[int] = None
    user_id: int
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ProfileModelSchema(ProfileCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
