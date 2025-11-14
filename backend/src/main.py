from typing import Union

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.api_v0.auth.router import router as auth_router
from src.api_v0.common.errors import BaseAppException
from src.config import settings
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI(title="KezdesuAI API")
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


@app.exception_handler(BaseAppException)
async def base_app_exception_handler(request: Request, exc: BaseAppException) -> Union[JSONResponse, Response]:
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
