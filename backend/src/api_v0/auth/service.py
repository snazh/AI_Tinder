from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.service import BaseService
from src.config import settings
from src.api_v0.users.schemas import UserModelSchema
from src.database.models.user import User, UserRole


class AuthService(BaseService[User, UserModelSchema]):
    def __init__(self):

        super().__init__(User, UserModelSchema)




