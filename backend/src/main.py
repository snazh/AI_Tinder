from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.api_v0.auth.router import router as auth_router
from src.config import settings

app = FastAPI(title="KezdesuAI API")

app.add_middleware(SessionMiddleware, secret_key=settings.auth.SECRET_KEY)
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",],  # можно ограничить ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)



