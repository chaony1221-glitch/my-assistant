from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat import ChatRequest
from app.services.llm import LLM


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("")
def chat(req: ChatRequest):
    messages = [
        message.model_dump()
        for message in req.messages
    ]

    llm = LLM()

    return StreamingResponse(
        llm.chat(messages),
        media_type="text/plain"
    )