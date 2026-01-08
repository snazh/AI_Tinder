
import asyncio

from src.redis_service.dependencies import get_email_queue, get_ai_task_queue
from src.email_client.setup import send_email


async def email_worker():
    print("Email worker started...")
    queue = get_email_queue()
    while True:
        email_task = await queue.pop_task()
        print("Processing email task:", email_task)
        subject = "Welcome to the Kezdesu AI"
        body = """
        Привет!

        Мы рады приветствовать тебя в Kezdesu AI — платформе для поиска друзей и новых интересных встреч!
        
        Теперь у тебя есть возможность:
        - Находить людей с похожими интересами
        - Планировать встречи и активности
        - Общаться и заводить настоящие дружеские связи
        
        Начни своё путешествие прямо сейчас и открой для себя новых друзей!
        
        👉 [Начать знакомство](https://kezdesu.ai)
        
        С любовью,  
        Команда Kezdesu AI 💛

        """
        send_email(email_task['email'], subject, body)
        print("Email task done:", email_task)


async def ai_worker():
    print("AI worker started...")
    queue = get_ai_task_queue()
    while True:
        ai_task = await queue.pop_task()
        print("Processing AI task:", ai_task)
        # тут выполняешь реальную работу, например, отправку письма

        print("AI task done:", ai_task)


async def run_workers():
    await asyncio.gather(email_worker(), ai_worker())


if __name__ == "__main__":
    asyncio.run(run_workers())
