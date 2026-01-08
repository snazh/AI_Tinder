from sqlalchemy.ext.asyncio import AsyncSession
from src.api_v0.common.service import BaseService
from src.api_v0.users.schemas import UserModelSchema, UserAuthSchema
from src.database.models.user import User
from src.redis_service.dependencies import get_email_queue, Queue
from fastapi import Depends


class AuthService(BaseService[User, UserModelSchema]):
    def __init__(self):
        super().__init__(User, UserModelSchema)

    async def google_auth(self,
                          user_data: UserAuthSchema,
                          session: AsyncSession
                          ) -> UserModelSchema:
        user = await self.get_one_by(field="sub", value=user_data.sub, session=session)

        if user is None:
            email_queue = get_email_queue()
            user = await super().create(item_data=user_data, session=session)
            # redis_service email broker

            await email_queue.push_task(task={"email": user.email})
        return user
