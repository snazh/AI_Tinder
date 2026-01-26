from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session

async def create_user_profile(session: AsyncSession=Depends(get_async_session)):

