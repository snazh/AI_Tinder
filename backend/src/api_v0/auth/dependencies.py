# from fastapi.security import OAuth2PasswordBearer
# from src.models.user import UserRole
# from src.api_v1.auth.service import AuthService
# from fastapi import Request, Response, Depends
# from src.api_v1.auth.errors import NotAuthorizedError, InvalidTokenError, AccessForbiddenError, TokenExpiredError
# from src.api_v1.auth.utils import jwt_util
# from src.config import settings
# from src.api_v1.auth.schemas import UserPayloadSchema
# from typing import Annotated
#
#
# # dependency injection for Authentication service
# def get_auth_service():
#     return AuthService()
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)
#
#
# def get_current_user(
#         request: Request,
#         response: Response,
#         token: Annotated[str, Depends(oauth2_scheme)]
# ) -> UserPayloadSchema:
#     access_token = request.cookies.get("access_token") or token
#     refresh_token = request.cookies.get("refresh_token")
#
#     if not access_token:
#         raise NotAuthorizedError()
#
#     try:
#         return jwt_util.verify_token(access_token)
#     # refresh token if access token is expired
#     except TokenExpiredError:
#
#         if not refresh_token:
#             raise NotAuthorizedError()
#         try:
#             payload = jwt_util.verify_token(refresh_token)
#             new_access_token = jwt_util.create_token(
#                 {"user_id": str(payload.user_id), "role": payload.role},
#                 token_type="access"
#             )
#             response.set_cookie(
#                 key="access_token",
#                 value=new_access_token,
#                 httponly=True,
#                 secure=True,
#                 samesite="lax",
#                 max_age=60 * settings.auth.ACCESS_TOKEN_EXPIRES_MINUTES,
#             )
#             return payload
#         except Exception:
#             raise InvalidTokenError()
#     except Exception:
#         raise InvalidTokenError()
#
#
# def require_role(*allowed_roles: UserRole):
#     def dependency(current_user: UserPayloadSchema = Depends(get_current_user)):
#         if current_user.role not in allowed_roles:
#             raise AccessForbiddenError
#
#     return Depends(dependency)
