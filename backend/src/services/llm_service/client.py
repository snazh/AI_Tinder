from openai import OpenAI
from src.config import settings

client = OpenAI(
    base_url=f"{settings.llm.llm_url}/v1",
    api_key="ollama"  # любой текст
)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
print(ask_llm(""))