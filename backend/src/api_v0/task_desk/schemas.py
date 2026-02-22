from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskCreateSchema(BaseModel):
    title: str
    price: float
    user_id: int
    description: str
    model_config = ConfigDict(from_attributes=True)


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    user_id: int
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class TaskModelSchema(TaskCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
