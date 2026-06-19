from collections.abc import Generator

from app.services.extractors.weather import extract_city
from app.services.llm import LLM
from app.tools.weather import weather_tool


def simple_agent(messages: list[dict]) -> Generator[str, None, None]:
    llm = LLM()
    user_message = messages[-1]["content"]

    if "天气" in user_message:
        city = extract_city(user_message)
        weather = weather_tool(city)

        if weather is None:
            yield "天气查询失败，请稍后再试。"
            return

        tool_prompt = f"""
用户问题：{user_message}

天气工具返回：
{weather.model_dump()}

请根据天气工具结果，用自然语言简洁回答用户。
"""

        yield from llm.stream_chat([
            {
                "role": "user",
                "content": tool_prompt,
            }
        ])

        return

    yield from llm.stream_chat(messages)
