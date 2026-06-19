from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat import ChatRequest
from app.services.agent import simple_agent


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("")
def chat(req: ChatRequest):
    messages = [
        message.model_dump()
        for message in req.messages
    ]

    return StreamingResponse(
        simple_agent(messages),
        media_type="text/plain",
    )
