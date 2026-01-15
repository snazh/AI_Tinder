from .celery_app import celery_app
import time

from src.email_client.setup import send_email


@celery_app.task
def send_welcome_email(email: str):
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
    send_email(email, subject, body)
    print("Welcome message send to email", email)
