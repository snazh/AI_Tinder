from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.api_v0.auth.router import router as auth_router
from src.api_v0.profile.router import router as profile_router
from src.api_v0.common.errors import BaseAppException
from src.config import settings
from starlette.middleware.sessions import SessionMiddleware
from src.core.logging_config import setup_logging
from src.services.redis_service.connection import create_redis

from meilisearch_python_sdk import AsyncClient
from src.services import meilisearch


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    setup_logging()
    app.state.redis = await create_redis()
    meilisearch.meili_client = AsyncClient(
        settings.meilisearch.MEILI_HTTP_ADDR,
        settings.meilisearch.MEILI_MASTER_KEY,
    )
    yield
    await app.state.redis.close()
    await meilisearch.meili_client.aclose()

app = FastAPI(title="KezdesuAI API", lifespan=lifespan)


def get_redis(request: Request):
    return request.app.state.redis


app.add_middleware(SessionMiddleware, secret_key=settings.auth.SECRET_KEY)
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", ],  # можно ограничить ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)


@app.exception_handler(BaseAppException)
async def base_app_exception_handler(request: Request, exc: BaseAppException) -> Union[JSONResponse, Response]:
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "Failure", "msg": exc.detail},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "Failure", "msg": exc.detail},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> Union[JSONResponse, Response]:
    return JSONResponse(
        status_code=500,
        content={"status": "Failure", "msg": f"Internal Server Error: {exc}"},
    )
