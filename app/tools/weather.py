from typing import Any

import requests

from app.models.weather import WeatherResponse


def get_weather(city: str) -> dict[str, Any] | None:
    """查询指定城市的天气情况。"""
    url = f"https://wttr.in/{city}?format=j1&lang=zh"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"请求失败！错误信息: {e}")
        return None
    except ValueError:
        print("天气数据解析失败！")
        return None

    return data


def format_weather(city: str, data: dict[str, Any]) -> WeatherResponse:
    """格式化天气数据。"""
    current = data["current_condition"][0]
    return WeatherResponse(
        city=city,
        weather=current["weatherDesc"][0]["value"],
        temp=f"{current['temp_C']} ℃",
    )


def weather_tool(city: str | None) -> WeatherResponse | None:
    """天气查询工具入口。"""
    if not city:
        return None

    data = get_weather(city)
    if data is None:
        return None
    return format_weather(city, data)
