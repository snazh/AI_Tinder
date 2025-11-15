from typing import Type, Optional
from urllib.request import Request

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.service import BaseService
from src.config import settings
from src.api_v0.profile.schemas import ProfileCreateSchema, ProfileModelSchema
from src.database.models import Profile


class ProfileService(BaseService[Profile, ProfileModelSchema]):
    def __init__(self):
        super().__init__(Profile, ProfileModelSchema)

