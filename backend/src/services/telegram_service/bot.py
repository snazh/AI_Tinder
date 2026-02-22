import asyncio
import httpx

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.config import settings

dp = Dispatcher()


def parse_start_token(text: str) -> str | None:
    parts = (text or "").split(maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else None


@dp.message(CommandStart())
async def start_handler(message: Message):
    token = parse_start_token(message.text or "")
    if not token:
        await message.answer("Открой ссылку подтверждения из приложения и нажми Start.")
        return

    chat_id = message.chat.id
    username = message.from_user.username if message.from_user else None

    url = settings.tg.BACKEND_PUBLIC_URL.rstrip("/") + "/api_v0/telegram/verify"

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(url, json={"token": token, "chat_id": chat_id, "username": username})

    if r.status_code == 200 and r.json().get("ok") is True:
        await message.answer("✅ Telegram подтверждён. Возвращайся в приложение.")
    else:
        await message.answer("❌ Токен неверный/истёк или уже использован.")


async def main():
    bot = Bot(token=settings.tg.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())