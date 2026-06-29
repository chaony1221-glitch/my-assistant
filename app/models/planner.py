from pydantic import BaseModel


class ToolDecision(BaseModel):
    tool: str | None
    arguments: dict = {}