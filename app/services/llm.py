from openai import OpenAI
from collections.abc import Generator

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

class LLM:

    def chat(self, messages: list[dict]) -> Generator[str, None, None]:
        stream = client.chat.completions.create(
            model="qwen3.6",
            messages=messages,
            stream=True  #开启流式输出
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                yield content