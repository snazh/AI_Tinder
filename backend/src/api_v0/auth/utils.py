from datetime import datetime, timedelta
from jose import jwt
from src.config import settings
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.auth.GOOGLE_CLIENT_ID,
    client_secret=settings.auth.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "email openid profile"}
)


class JWTUtil:
    @staticmethod
    def create_access_token(data: dict):

        payload = data.copy()
        payload.update({
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "type": "access"  # <-- вот это поле
        })
        token = jwt.encode(payload, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)
        return token

    @staticmethod
    def create_refresh_token(data: dict):

        payload = data.copy()
        payload.update({
            "exp": datetime.utcnow() + timedelta(days=7),
            "type": "refresh"  # <-- вот это поле
        })
        token = jwt.encode(payload, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)
        return token

    @staticmethod
    def decode_token(token: str):
        return jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
