
from fastapi import Request, Response, Depends, HTTPException
from jose import jwt
from src.api_v0.auth.errors import TokenError, AuthError
from src.api_v0.auth.service import AuthService
from src.config import settings


# dependency injection for Authentication service
def get_auth_service() -> AuthService:
    return AuthService()


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise AuthError(message="Not Authorized")
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])

        if payload.get("type") != "access":
            raise TokenError(message="Invalid token type")
        return payload
    except TokenError:
        raise
    except Exception:
        raise TokenError(message="Invalid token")

#
# def require_role(*allowed_roles: UserRole):
#     def dependency(current_user: UserPayloadSchema = Depends(get_current_user)):
#         if current_user.role not in allowed_roles:
#             raise AccessForbiddenError
#
#     return Depends(dependency)
