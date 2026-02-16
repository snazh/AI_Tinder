import pytest
import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from src.main import app
from src.api_v0.auth.dependencies import get_current_user

# ✅ ВАЖНО: поменяй на реальный импорт зависимости, которая выдаёт AsyncSession
from src.database.db import get_async_session

TEST_DB_URL = "postgresql+asyncpg://postgres:10112005@localhost:5432/test_db"

engine = create_async_engine(TEST_DB_URL, future=True,poolclass=NullPool)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
def override_user():
    async def _override():
        return {"id": 1, "role": "user", "email": "test@test.local"}
    return _override


@pytest.fixture
async def db_session():
    async with engine.connect() as conn:
        # ✅ Сбросить таблицы + sequence ДО теста (и зафиксировать это)
        await conn.execute(text("TRUNCATE users, profiles, likes RESTART IDENTITY CASCADE;"))
        await conn.commit()

        session = TestSessionLocal(bind=conn)

        try:
            yield session
        finally:
            # ✅ На всякий случай: откатить незакоммиченные изменения теста
            await session.rollback()
            await session.close()


@pytest.fixture
async def client(db_session, override_user):
    async def _get_db_override():
        yield db_session

    app.dependency_overrides[get_async_session] = _get_db_override
    app.dependency_overrides[get_current_user] = override_user

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
