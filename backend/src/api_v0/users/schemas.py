from datetime import datetime

from httptools.parser.parser import Optional
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
    telegram_chat_id: Optional[int]
    telegram_username: Optional[int]
    telegram_verified_at: Optional[int]