from sqlalchemy.ext.asyncio import AsyncSession
from src.api_v0.common.service import BaseRepo
from src.api_v0.users.schemas import UserModelSchema, UserAuthSchema
from src.database.models.user import User


class AuthService(BaseRepo[User, UserModelSchema]):
    def __init__(self):
        super().__init__(User, UserModelSchema)

    async def google_auth(self,
                          user_data: UserAuthSchema,
                          session: AsyncSession
                          ) -> tuple[UserModelSchema, bool]:
        is_new = False
        user = await super().get_one_by(field="sub", value=user_data.sub, session=session)

        if user is None:
            user = await super().create(item_data=user_data, session=session)
            is_new = True

        return user, is_new
