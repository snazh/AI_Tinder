from fastapi import APIRouter, Request, HTTPException, Response, Depends, status
from authlib.integrations.starlette_client import OAuth, OAuthError
from jose import jwt

from src.api_v0.auth.utils import JWTUtil
from src.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.auth.GOOGLE_CLIENT_ID,
    client_secret=settings.auth.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "email openid profile"}
)


# 1) Login — редирект на Google
@router.get("/login", status_code=status.HTTP_200_OK)
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.auth.REDIRECT_URL)


# 2) Auth — получает токен от Google и ставит JWT в куки
@router.get("/", name="auth")
async def auth(request: Request, response: Response):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=400, detail="Invalid Google OAuth token")

    user = token.get("userinfo")
    if not user:
        raise HTTPException(status_code=403, detail="Authentication failed")

    user_data = {
        "sub": user["sub"],
        "email": user["email"],
        "name": user.get("name"),
        "picture": user.get("picture")
    }

    access_token = JWTUtil.create_access_token(user_data)
    refresh_token = JWTUtil.create_refresh_token(user_data)

    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax")

    return {"message": "Logged in successfully", "user": user_data}


# 3) Декодирование JWT из куки
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
        print(payload)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# 4) Профиль пользователя
@router.get("/profile")
def profile(user: dict = Depends(get_current_user)):
    return {"user": user}


# 5) Refresh токена
@router.post("/refresh")
def refresh_token(request: Request, response: Response):
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
