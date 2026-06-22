from collections.abc import Generator

from openai import OpenAI

from app.core.config import settings
from app.prompts.system import CHAT_SYSTEM_PROMPT


client = OpenAI(
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
)

class LLM:
    def chat(self, messages: list[dict]) -> str:
        response = client.chat.completions.create(
            model=settings.extractor_model,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content

    def stream_chat(self, messages: list[dict]) -> Generator[str, None, None]:
        stream = client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {
                    "role": "system",
                    "content": CHAT_SYSTEM_PROMPT,
                },
                *messages,
            ],
            stream=True,
        )

        started = False

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if not content:
                continue

            if not started:
                content = content.lstrip()
                if not content:
                    continue
                started = True

            if content:
                yield content
