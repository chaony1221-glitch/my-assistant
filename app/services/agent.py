from collections.abc import Generator

from app.services.llm import LLM
from app.tools.weather_tool import weather_tool
from app.services.extractor.weather import extract_city

def simple_agent(messages: list[dict]) -> Generator[str, None, None]:
    user_message = messages[-1]["content"]

    # 判断是否进行工具调用
    if "天气" in user_message:
        # 让llm从用户提示词中提取城市
        city = extract_city(user_message)

        weather = weather_tool(city)
        print(city)

        if weather is None:
            yield "天气查询失败，请稍后再试。"
            return

        # 将工具返回结果包装后重新扔给大模型，让它输出自然语言
        tool_prompt = f"""
用户问题：{user_message}

天气工具返回：
{weather.model_dump()}

请根据天气工具结果，用自然语言简洁回答用户。
"""
        llm = LLM()

        yield from llm.stream_chat([
            {
                "role": "user",
                "content": tool_prompt
            }
        ])

        return
    
    #不走工具 常规chat
    yield from llm.stream_chat(messages)