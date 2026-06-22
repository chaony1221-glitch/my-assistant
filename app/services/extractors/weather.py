from app.prompts.weather import build_extract_city_prompt
from app.services.llm import LLM


def extract_city(user_message: str) -> str | None:
    """从用户提问中提取城市名称。"""
    llm = LLM()

    prompt = build_extract_city_prompt(user_message)

    city = llm.chat([
        {
            "role": "user",
            "content": prompt,
        }
    ]).strip()

    return city or None
