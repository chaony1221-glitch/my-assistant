from app.models.weather import WeatherResponse


def build_extract_city_prompt(user_message: str) -> str:
    return f"""
请从下面的话中提取城市名称。

要求：
1. 只返回城市名。
2. 不要解释。
3. 没有城市返回空字符串。

用户输入：
{user_message}
"""


def build_weather_answer_prompt(
    user_message: str,
    weather: WeatherResponse,
) -> str:
    return f"""
用户问题：{user_message}

天气工具返回：
{weather.model_dump()}

请根据天气工具结果，用自然语言简洁回答用户。
"""
