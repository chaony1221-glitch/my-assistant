from collections.abc import Generator

from app.prompts.weather import build_weather_answer_prompt
from app.services.llm import LLM
from app.tools.weather import weather_tool
from app.tools.decide import decide_tool

def simple_agent(messages: list[dict]) -> Generator[str, None, None]:
    llm = LLM()

    user_message = messages[-1]["content"]

    print("====USER_MESSAGE===")
    print(user_message)
    print("==============")


    decision = decide_tool(messages)
    print(decision)
    
    if decision.tool == "weather":
        city = decision.arguments.get("city")

        if not city:
            yield "你想查询哪个城市的天气？"
            return 
        
        weather = weather_tool(city)

        if weather is None:
            yield f"没有查询到{city}的天气。"
            return
        
        tool_prompt = build_weather_answer_prompt(user_message, weather)

        print("====== TOOL PROMPT ======")
        print(tool_prompt)
        print("=========================")

        yield from llm.stream_chat([
            {
                "role": "user",
                "content": tool_prompt
            }
        ])

        return

