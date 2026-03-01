from datetime import datetime, timezone
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.api_v0.telegram.schemas import TelegramLinkOut, TelegramVerifyIn
from src.api_v0.users.dependencies import get_user_service
from src.api_v0.users.service import UserService
from src.config import settings
from src.services.redis_service.connection import get_redis
from src.database.db import get_async_session
from src.api_v0.auth.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/telegram", tags=["telegram"])

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
    try:
        key = f"tg_verify:{payload.token}"

        user_id = int(await redis.get(key))
        if not user_id:
            raise HTTPException(status_code=400, detail="Token invalid or expired")

        await user_service.get_profile_by(field="id", value=user_id, session=session)

        is_bind = await user_service.bind_telegram(user_id=user_id, chat_id=payload.chat_id, username=payload.username,
                                                   session=session)

        if not is_bind:
            raise HTTPException(status_code=400, detail="Failed to bind telegram")
        await session.commit()
        await redis.delete(key)
        logger.info(f"Telegram {payload.username} was bind to user", extra={"user_id": user_id})
        return {"msg": "telegram is bind"}
    except Exception:
        await session.rollback()
        raise
