from fastapi import APIRouter

from app.schemas.interaction import AgentChatRequest, AgentChatResponse
from app.services.agent_service import chat_with_agent

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/chat", response_model=AgentChatResponse)
def chat(payload: AgentChatRequest):
    response = chat_with_agent(
        user_message=payload.user_message,
        current_form=payload.current_form.model_dump() if payload.current_form else None,
    )
    return AgentChatResponse(**response)
