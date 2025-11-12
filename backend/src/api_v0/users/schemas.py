from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from src.database.models.user import UserRole


class UserModelSchema(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)