from datetime import datetime, timezone
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.telegram.schemas import TelegramLinkOut, TelegramVerifyIn
from src.api_v0.users.dependencies import get_user_service
from src.api_v0.users.service import UserService
from src.config import settings
from src.services.redis_service.connection import get_redis
from src.database.db import get_async_session
from src.api_v0.auth.dependencies import get_current_user
from src.database.models.user import User

router = APIRouter(prefix="/api_v0/telegram", tags=["telegram"])

TOKEN_TTL_SECONDS = 10 * 60


@router.post("/link", response_model=TelegramLinkOut)
async def create_telegram_link(
        user: dict = Depends(get_current_user),
        redis: Redis = Depends(get_redis),
):
    token = secrets.token_urlsafe(24)
    key = f"tg_verify:{token}"

    await redis.set(key, str(user["id"]), ex=TOKEN_TTL_SECONDS)

    bot_username = settings.tg.BOT_USERNAME
    url = f"https://t.me/{bot_username}?start={token}"

    return TelegramLinkOut(url=url, token=token)


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_telegram(
        payload: TelegramVerifyIn,
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis),
        user_service: UserService = Depends(get_user_service)
):
    key = f"tg_verify:{payload.token}"

    user_id = await redis.get(key)
    if not user_id:
        raise HTTPException(status_code=400, detail="Token invalid or expired")

    user = await user_service.get_profile_by(field="id", value=int(user_id), session=session)


    user.telegram_chat_id = payload.chat_id
    user.telegram_username = payload.username
    user.telegram_verified_at = datetime.now(timezone.utc)

    await session.commit()
    await redis.delete(key)

    return {"ok": True}
