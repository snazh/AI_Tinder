from fastapi import APIRouter, Request
from src.config import settings
from authlib.integrations.starlette_client import OAuth

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login")
async def login(request: Request):
    request.session.clear()
    referer = request.headers.get("referer")
    frontend_url = settings.auth.FRONTEND_URL
    redirect_url = settings.auth.REDIRECT_URL
    request.session["login_redirect"] = frontend_url

    return await oauth.auth_demo.authorize_redirect(request, redirect_url, prompt="consent")
