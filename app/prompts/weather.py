from app.models.weather import WeatherResponse

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
