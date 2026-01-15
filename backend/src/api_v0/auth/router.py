from fastapi import APIRouter, Request, HTTPException, Response, Depends, status
from authlib.integrations.starlette_client import OAuth, OAuthError
from jose import jwt
from src.api_v0.auth.dependencies import get_current_user, get_auth_service
from src.api_v0.auth.service import AuthService
from src.api_v0.auth.utils import JWTUtil, oauth
from src.config import settings
from src.api_v0.auth.errors import TokenError, AuthError
from src.api_v0.users.schemas import UserAuthSchema
from src.database.models.user import UserRole
from src.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.tasks.email_tasks import send_welcome_email

router = APIRouter(prefix="/auth", tags=["Auth"])


# 1) Login — редирект на Google
@router.get("/login", status_code=status.HTTP_200_OK)
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.auth.REDIRECT_URL)


# 2) Auth — получает токен от Google и ставит JWT в куки
@router.get("/", name="auth")
async def auth(request: Request,
               response: Response,
               service: AuthService = Depends(get_auth_service),
               session: AsyncSession = Depends(get_async_session)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise TokenError("Invalid Google OAuth token")

    user = token.get("userinfo")
    if not user:
        raise AuthError(message="Authentication failed")
    user_data = UserAuthSchema(sub=user["sub"], email=user["email"], role=UserRole.user)

    user, is_new = await service.google_auth(user_data=user_data, session=session)

    # create tokens
    user_payload = {
        "id": user.id,
        "role": user.role.value,
        "email": user.email,
        "sub": user.sub
    }
    access_token = JWTUtil.create_access_token(user_payload)
    refresh_token = JWTUtil.create_refresh_token(user_payload)
    # create cookies with tokens
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax")
    if is_new:
        send_welcome_email.delay(user.email)
    return {"message": "Logged in successfully", "user": user}


# 4) Профиль пользователя
@router.get("/profile")
def profile(user: dict = Depends(get_current_user)):
    return {"message": "Profile fetched", "user": user}


# 5) Refresh токена
@router.post("/refresh")
def refresh(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = JWTUtil.create_access_token({
        "sub": payload["sub"],
        "email": payload["email"],
        "name": payload.get("name"),
        "picture": payload.get("picture")
    })

    response.set_cookie(key="access_token", value=new_access_token, httponly=True, samesite="lax")
    return {"message": "Access token refreshed"}


# 6) Logout — удаляем куки
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
