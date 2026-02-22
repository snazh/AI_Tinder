from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.errors import ItemNotFoundError
from src.api_v0.common.service import BaseService
from src.api_v0.users.schemas import UserModelSchema, UserAuthSchema
from src.database.models.user import User

import logging

logger = logging.getLogger(__name__)
class UserService(BaseService[User, UserModelSchema]):
    def __init__(self):
        super().__init__(User, UserModelSchema)
    async def get_profile_by(self, field: str, value, session: AsyncSession) -> UserModelSchema:
        if field == "id":
            user = await super().get_by_id(item_id=value, session=session)
        else:
            user = await super().get_one_by(field=field, value=value, session=session)
        if user is None:
            logger.warning(f"User with {field}:{value} does not exist")
            raise ItemNotFoundError(item="user", attr=field, value=value)
        return user
