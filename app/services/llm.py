from openai import OpenAI
from collections.abc import Generator

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

SYSTEM_PROMPT = """
你是一个简洁、直接的中文 AI 助手。
不要输出思考过程，只输出最终答案。
"""

class LLM:
    def chat(self, messages: list[dict]) -> str:
        response = client.chat.completions.create(
            model="qwen3.6",
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content

    def stream_chat(self, messages: list[dict]) -> Generator[str, None, None]:
        
        stream = client.chat.completions.create(
            model="qwen/qwen3.6-35b-a3b",
            messages=[
                # 添加SYSTEM_PROMPT，放在用户提示词之前
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages
            ],
            stream=True  #开启流式输出
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