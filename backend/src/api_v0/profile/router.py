import json

from fastapi import APIRouter, Request, HTTPException, Response, Depends, status, Form, File, UploadFile, Body
from src.api_v0.auth.dependencies import get_current_user
from src.api_v0.profile.dependencies import get_profile_service
from src.api_v0.profile.schemas import ProfileCreateSchema
from src.api_v0.profile.service import ProfileService

from src.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.s3service.dependencies import get_media_service
from src.s3service.service import MediaService, MediaSection


router = APIRouter(prefix="/profile", tags=["Auth"])


# @router.get("/", status_code=status.HTTP_200_OK)
# async def get_profile(request: Request):
#     pass


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(
        profile_data: str = Form(...),
        avatar: UploadFile = File(...),
        user: dict = Depends(get_current_user),
        service: ProfileService = Depends(get_profile_service),
        session: AsyncSession = Depends(get_async_session),
        media_service: MediaService = Depends(get_media_service)):
    avatar_path = await media_service.save_image_s3(uploaded_file=avatar, section=MediaSection.profile)
    user_id = user["id"]
    profile_schema = ProfileCreateSchema(**json.loads(profile_data), user_id=user_id, avatar_path=avatar_path)
    new_profile = await service.create(item_data=profile_schema, session=session)
    return {"message": "Profile created successfully", "profile": new_profile}
