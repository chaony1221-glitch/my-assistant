from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: str | None = None


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)


class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessage]
