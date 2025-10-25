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


class GoogleAuthSettings(CoreConfig):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    JWT_SECRET_KEY: str
    SECRET_KEY: str
    REDIRECT_URL:str
    FRONTEND_URL:str
# class AuthSettings(CoreConfig):
#     JWT_SECRET_KEY:str
#     SECRET_KEY:str
#     ALGO: str
class RedisSetting(CoreConfig):
    REDIS_HOST: str
    REDIS_PORT: int


class Settings(CoreConfig):
    db: DBSettings = DBSettings()
    auth: GoogleAuthSettings = GoogleAuthSettings()
    redis: RedisSetting = RedisSetting()


settings = Settings()
