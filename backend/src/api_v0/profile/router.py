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
router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(
        profile_data: str = Form(...),
        avatar: UploadFile = File(...),
        user: dict = Depends(get_current_user),
        service: ProfileService = Depends(get_profile_service),
        session: AsyncSession = Depends(get_async_session),
        media_service: MediaService = Depends(get_media_service),
        meili_service: AsyncClient = Depends(get_meili_client)):
    try:
        data_dict = json.loads(profile_data)
        if avatar.filename == "":
            raise HTTPException(status_code=422, detail="No file provided")
    except JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON format")

    avatar_path = await media_service.save_image_s3(uploaded_file=avatar, section=MediaSection.profile)

    try:
        user_id = user["id"]
        profile_schema = ProfileCreateSchema(**data_dict, user_id=user_id, avatar_path=avatar_path)

        new_profile = await service.create(item_data=profile_schema, session=session)
        logger.info(
            "Profile created successfully",
            extra={"user_id": new_profile.user_id},
        )
        # adding to meilisearch
        document = new_profile.model_dump(mode="json")
        index = meili_service.index("profiles")
        await index.add_documents([document])
        await session.commit()  # commit transaction
        return {"msg": "Profile created successfully", "profile": new_profile}
    except Exception as e:
        logger.error(
            f"Profile creation failed:{e}",
            extra={"user_id": user["id"]},
        )
        await media_service.delete_image(avatar_path)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Profile creation failed")


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_profiles(query: str, limit: int = 20, meili_service: AsyncClient = Depends(get_meili_client)):
    index = meili_service.index("profiles")
    results = await index.search(query, limit=limit)
    return results.hits


@router.get("/{profile_id}", status_code=status.HTTP_200_OK)
async def get_profile(profile_id: int,
                      user: dict = Depends(get_current_user),
                      service: ProfileService = Depends(get_profile_service),
                      session: AsyncSession = Depends(get_async_session),
                      media_service: MediaService = Depends(get_media_service)):
    profile = await service.get_by_id(item_id=profile_id, session=session)
    if profile is None:
        raise ItemNotFoundError(item="profile", attr="id", value=profile_id)
    avatar_path = await media_service.get_image_link(key_path=profile.avatar_path)
    return {
        "msg": f"Profile with ID: {profile_id} fetched",
        "data": {
            "profile": profile,
            "avatar": avatar_path
        }
    }


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int,
                         user: dict = Depends(get_current_user),
                         service: ProfileService = Depends(get_profile_service),
                         session: AsyncSession = Depends(get_async_session),
                         media_service: MediaService = Depends(get_media_service)):
    profile = await service.get_by_id(item_id=profile_id, session=session)
    if profile is None:
        raise ItemNotFoundError("profile", attr="id", value=profile_id)

    if user["role"] != "admin" and profile["user_id"] != user["id"]:
        raise AccessForbiddenError()

    await service.delete(item_id=profile_id, session=session)
    await media_service.delete_image(profile.avatar_path)


@router.put("/{profile_id}", status_code=status.HTTP_200_OK)
async def update_profile(profile_id: int,
                         profile_update_data: str = Form(...),
                         avatar: UploadFile = File(...),
                         user: dict = Depends(get_current_user),
                         service: ProfileService = Depends(get_profile_service),
                         session: AsyncSession = Depends(get_async_session),
                         media_service: MediaService = Depends(get_media_service)):
    try:
        data_dict = json.loads(profile_update_data)
    except JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON format")
    profile = await service.get_by_id(item_id=profile_id, session=session)
    if profile is None:
        raise ItemNotFoundError(item="profile", attr="id", value=profile_id)
    if user["role"] != "admin" and profile["user_id"] != user["id"]:
        raise AccessForbiddenError()
    old_avatar_path = profile.avatar_path
    new_avatar_path = None
    try:
        if avatar and avatar.filename:
            new_avatar_path = await media_service.save_image_s3(uploaded_file=avatar,
                                                                section=MediaSection.profile)

        profile_schema = ProfileUpdateSchema(**data_dict, user_id=profile.user_id,
                                             avatar_path=new_avatar_path or old_avatar_path)

        await service.update(item_id=profile_id, item_update_data=profile_schema, session=session)
        if new_avatar_path and old_avatar_path:
            await media_service.delete_image(key_path=old_avatar_path)
        return {"msg": "Profile updated successfully"}
    except Exception:
        logger.error(
            "Profile update failed",
            extra={"user_id": user["id"]},
        )
        if new_avatar_path:
            await media_service.delete_image(key_path=new_avatar_path)
        raise HTTPException(status_code=500, detail="Profile update failed")


@router.post("/{profile_id}/like", status_code=status.HTTP_201_CREATED)
async def like_profile(profile_id: int,
                       user: dict = Depends(get_current_user),
                       service: LikeService = Depends(get_like_service),
                       profile_service: ProfileService = Depends(get_profile_service),
                       session: AsyncSession = Depends(get_async_session)):
    profile = await profile_service.get_profile_by(field="user_id", value=user["id"], session=session)
    like_data = LikeCreateSchema(liked_id=profile_id, liker_id=profile.id)
    like = await service.like_profile(like_data=like_data, session=session)
    logger.info(f"Profile with ID: {profile_id} was liked by profile with ID:{profile.id}", extra={"user_id": user["id"]})
    return {"msg": f"Profile with ID: {profile_id} liked at {like.created_at}"}


@router.get("/{profile_id}/likers", status_code=status.HTTP_200_OK)
async def get_likers(profile_id: int,
                     user: dict = Depends(get_current_user),
                     service: LikeService = Depends(get_like_service),
                     profile_service: ProfileService = Depends(get_profile_service),
                     session: AsyncSession = Depends(get_async_session)):
    my_profile = await profile_service.get_profile_by(field="user_id", value=user["id"], session=session)

    #checks if profile exists.
    await profile_service.get_profile_by(field="id", value=profile_id, session=session)

    if my_profile.id != profile_id:
        logger.warning(f"Not authorized access to profile with ID:{profile_id}", extra={"user_id": user["id"]})
        raise AccessForbiddenError()

    likers = await service.find_likers(profile_id=profile_id, session=session)
    logger.info(f"Likers for profile with ID:{profile_id}", extra={"user_id": user["id"]})
    return likers
