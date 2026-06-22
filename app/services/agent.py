from collections.abc import Generator

from app.prompts.weather import build_weather_answer_prompt
from app.services.extractors.weather import extract_city
from app.services.intent import Intent, detect_intent
from app.services.llm import LLM
from app.tools.weather import weather_tool


def answer_with_weather(user_message: str, llm: LLM) -> Generator[str, None, None]:
    city = extract_city(user_message)
    weather = weather_tool(city)

    if weather is None:
        yield "天气查询失败，请稍后再试。"
        return

    tool_prompt = build_weather_answer_prompt(user_message, weather)

    yield from llm.stream_chat([
        {
            "role": "user",
            "content": tool_prompt,
        }
    ])


def simple_agent(messages: list[dict]) -> Generator[str, None, None]:
    llm = LLM()
    user_message = messages[-1]["content"]

    intent = detect_intent(user_message)

    if intent == Intent.WEATHER:
        yield from answer_with_weather(user_message, llm)
        return

    yield from llm.stream_chat(messages)
