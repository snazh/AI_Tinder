from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.errors import ItemNotFoundError, ItemAlreadyExistsError
from src.api_v0.common.service import BaseRepo
from src.api_v0.users.schemas import UserModelSchema, UserAuthSchema
from src.database.models.user import User

import logging

logger = logging.getLogger(__name__)


class UserService(BaseRepo[User, UserModelSchema]):
    def __init__(self):
        super().__init__(User, UserModelSchema)

    async def bind_telegram(self, user_id: int, chat_id: int, username: str, session: AsyncSession) -> bool:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(telegram_chat_id=chat_id, telegram_username=username, telegram_verified_at=datetime.now(timezone.utc))
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(stmt)
        await session.flush()
        return result.rowcount > 0

    async def get_profile_by(self, field: str, value, session: AsyncSession) -> UserModelSchema:
        if field == "id":
            user = await super().get_by_id(item_id=value, session=session)
        else:
            user = await super().get_one_by(field=field, value=value, session=session)
        if user is None:
            logger.warning(f"User with {field}:{value} does not exist")
            raise ItemNotFoundError(item="user", attr=field, value=value)
        return user
