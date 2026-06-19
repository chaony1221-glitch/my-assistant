from app.services.llm import LLM


def extract_city(user_message: str) -> str | None:
    """从用户提问中提取城市名称。"""
    llm = LLM()

    prompt = f"""
请从下面的话中提取城市名称。

要求：
1. 只返回城市名。
2. 不要解释。
3. 没有城市返回空字符串。

用户输入：
{user_message}
"""

    city = llm.chat([
        {
            "role": "user",
            "content": prompt,
        }
    ]).strip()

    return city or None
