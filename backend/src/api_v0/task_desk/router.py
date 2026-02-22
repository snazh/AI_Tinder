import json
from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, Depends, status, Form, File, UploadFile
from meilisearch_python_sdk import AsyncClient

from src.api_v0.common.errors import ItemNotFoundError

from src.api_v0.auth.dependencies import get_current_user
from src.api_v0.profile.dependencies import get_profile_service, get_like_service
from src.api_v0.profile.schemas import ProfileCreateSchema, ProfileUpdateSchema, LikeCreateSchema
from src.api_v0.profile.service import ProfileService, LikeService
from src.api_v0.auth.errors import AccessForbiddenError
from src.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.meilisearch_service.meilisearch import get_meili_client
from src.services.s3service.dependencies import get_media_service
from src.services.s3service.service import MediaService, MediaSection
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/task-desk", tags=["Task Desk"])


@router.post("/add", status_code=status.HTTP_200_OK)
async def create_task():
    pass