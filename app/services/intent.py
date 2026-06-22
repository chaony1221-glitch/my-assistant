from enum import Enum

WEATHER_KEYWORDS = [
    "天气",
    "气温",
    "温度",
    "多少度",
    "下雨",
    "下雪",
    "带伞",
    "出门",
    "冷不冷",
    "热不热",
    "冷吗",
    "热吗",
]


class Intent(str, Enum):
    CHAT = "chat"
    WEATHER = "weather"


def detect_intent(user_message: str) -> Intent:
    normalized_message = user_message.strip().lower()

    if any(
        keyword in normalized_message
        for keyword in WEATHER_KEYWORDS
    ):
        return Intent.WEATHER

    return Intent.CHAT
