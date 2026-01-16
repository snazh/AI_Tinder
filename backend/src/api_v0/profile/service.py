from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.service import BaseService
from src.config import settings
from src.api_v0.profile.schemas import ProfileCreateSchema, ProfileModelSchema
from src.database.models import Profile
import logging

logger = logging.getLogger(__name__)


class ProfileService(BaseService[Profile, ProfileModelSchema]):
    def __init__(self):
        super().__init__(Profile, ProfileModelSchema)

    async def create_profile(self, profile_data: ProfileCreateSchema, session: AsyncSession):
        profile = await super().create(item_data=profile_data, session=session)
        logger.info(
            "Profile created successfully",
            extra={"user_id": profile_data.user_id},
        )
        return profile



