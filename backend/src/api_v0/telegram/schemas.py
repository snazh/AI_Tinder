from pydantic import BaseModel

class TelegramVerifyIn(BaseModel):
    token: str
    chat_id: int
    username: str | None = None

class TelegramLinkOut(BaseModel):
    url: str
    token: str