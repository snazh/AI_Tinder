from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.errors import ItemNotFoundError
from src.api_v0.common.service import BaseService
from src.config import settings
from src.api_v0.profile.schemas import ProfileCreateSchema, ProfileModelSchema, LikeCreateSchema, LikeModelSchema
from src.database.models import Profile, Like, User
import logging

logger = logging.getLogger(__name__)


class ProfileService(BaseService[Profile, ProfileModelSchema]):
    def __init__(self):
        super().__init__(Profile, ProfileModelSchema)

    async def create_profile(self, profile_data: ProfileCreateSchema, session: AsyncSession) -> ProfileModelSchema:
        profile = await super().create(item_data=profile_data, session=session)
        return profile

    async def get_profile_by(self, field: str, value, session: AsyncSession) -> ProfileModelSchema:
        if field == "id":
            profile = await super().get_by_id(item_id=value, session=session)
        else:
            profile = await super().get_one_by(field=field, value=value, session=session)
        if profile is None:
            logger.warning(f"Profile with {field}:{value} does not exist")
            raise ItemNotFoundError(item="profile", attr=field, value=value)
        return profile


class LikeService(BaseService[Like, LikeModelSchema]):
    def __init__(self):
        super().__init__(Like, LikeModelSchema)

    async def like_profile(self, like_data: LikeCreateSchema, session: AsyncSession) -> LikeModelSchema:
        like = await super().create(item_data=like_data, session=session)
        return like

    async def find_likers(self, profile_id: int, session: AsyncSession) -> List[ProfileModelSchema]:
        stmt = (
            select(Profile)
            .join(self.model, Profile.id == self.model.liker_id)
            .where(self.model.liked_id == profile_id)  # liker profile
        )

        result = await session.execute(stmt)
        likers = []
        for profile in result.scalars().all():
            likers.append(ProfileModelSchema.model_validate(profile))
        return likers

    async def get_user_likes(self, profile_id: int, session: AsyncSession) -> List[ProfileModelSchema]:
        stmt = (
            select(Profile)
            .join(self.model, Profile.id == self.model.liker_id)
            .where(self.model.liker_id == profile_id)
        )
        result = await session.execute(stmt)
        likes = []
        for profile in result.scalars().all():
            likes.append(ProfileModelSchema.model_validate(profile))
        return likes

    async def find_mutual_like(self):
        pass
