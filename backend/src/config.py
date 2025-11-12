from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# declaring path to .env file
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ENV_PATH = os.path.join(ROOT_DIR, '.env')


class CoreConfig(BaseSettings):
    model_config = SettingsConfigDict(  # configuring .env file
        env_file=ENV_PATH,
        env_file_encoding='utf-8',
        extra="ignore")  # ignoring other secret keys


class DBSettings(CoreConfig):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def async_database_url(self) -> str:
        # Construct the async database URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AuthSettings(CoreConfig):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    REDIRECT_URL: str = "http://127.0.0.1:8000/auth"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class AdminSettings(CoreConfig):
    ADMIN_EMAIL: str


class RedisSetting(CoreConfig):
    REDIS_HOST: str
    REDIS_PORT: int


class Settings(CoreConfig):
    db: DBSettings = DBSettings()
    auth: AuthSettings = AuthSettings()
    admin_data: AdminSettings = AdminSettings()
    redis: RedisSetting = RedisSetting()


settings = Settings()
print(f"{settings.db.async_database_url}")
