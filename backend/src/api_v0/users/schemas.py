from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from src.database.models.user import UserRole


class UserAuthSchema(BaseModel):
    email: EmailStr
    sub: str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserModelSchema(UserAuthSchema):
    id: int
    created_at: datetime
    updated_at: datetime

