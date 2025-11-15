from typing import Type, Optional
from urllib.request import Request

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.service import BaseService
from src.config import settings
from src.api_v0.users.schemas import UserModelSchema, UserAuthSchema
from src.database.models.user import User, UserRole
from src.api_v0.auth.utils import oauth, JWTUtil


class AuthService(BaseService[User, UserModelSchema]):
    def __init__(self):
        super().__init__(User, UserModelSchema)

    async def google_auth(self, user_data: UserAuthSchema, session: AsyncSession) -> UserModelSchema:
        user = await self.get_one_by(field="sub", value=user_data.sub, session=session)

        if user is None:
            user = await super().create(item_data=user_data, session=session)

        return user
