from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProfileCreateSchema(BaseModel):
    username: str
    avatar_path: str
    user_id: int
    age: int
    description: str
    model_config = ConfigDict(from_attributes=True)


class ProfileModelSchema(ProfileCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
