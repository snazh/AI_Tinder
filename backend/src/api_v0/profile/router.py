import json
from json import JSONDecodeError

from fastapi import APIRouter, Request, HTTPException, Response, Depends, status, Form, File, UploadFile, Body
from pydantic import ValidationError

from src.api_v0.auth.dependencies import get_current_user
from src.api_v0.profile.dependencies import get_profile_service
from src.api_v0.profile.schemas import ProfileCreateSchema
from src.api_v0.profile.service import ProfileService

from src.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.s3service.dependencies import get_media_service
from src.s3service.service import MediaService, MediaSection
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(
        profile_data: str = Form(...),
        avatar: UploadFile = File(...),
        user: dict = Depends(get_current_user),
        service: ProfileService = Depends(get_profile_service),
        session: AsyncSession = Depends(get_async_session),
        media_service: MediaService = Depends(get_media_service)):
    try:
        data_dict = json.loads(profile_data)
    except JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON format")


    avatar_path = await media_service.save_image_s3(uploaded_file=avatar, section=MediaSection.profile)
    try:
        user_id = user["id"]
        profile_schema = ProfileCreateSchema(**data_dict, user_id=user_id, avatar_path=avatar_path)

        new_profile = await service.create(item_data=profile_schema, session=session)
        return {"msg": "Profile created successfully", "profile": new_profile}
    except Exception:
        logger.error(
            "Profile creation failed",
            extra={"user_id": user["id"]},
        )
        await media_service.delete_image(avatar_path)
        raise HTTPException(status_code=500, detail="Profile creation failed")


@router.get("/:profile_id")
async def get_profile(profile_id: int,
                      user: dict = Depends(get_current_user),
                      service: ProfileService = Depends(get_profile_service),
                      session: AsyncSession = Depends(get_async_session),
                      media_service: MediaService = Depends(get_media_service)):
    profile = await service.get_by_id(item_id=profile_id, session=session)

    avatar_path = await media_service.get_image_link(key_path=profile.avatar_path)
    return {
        "msg": f"Profile with ID: {profile_id} fetched",
        "data": {
            "profile": profile,
            "avatar": avatar_path
        }
    }
