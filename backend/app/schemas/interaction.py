from datetime import datetime

from pydantic import BaseModel, Field


class InteractionBase(BaseModel):
    hcp_name: str = Field(..., examples=["Dr. Asha Mehta"])
    interaction_type: str = "Meeting"
    interaction_datetime: datetime
    attendees: list[str] = []
    topics_discussed: str = ""
    materials_shared: list[str] = []
    samples_distributed: list[str] = []
    sentiment: str = "Neutral"
    outcomes: str = ""
    follow_up_actions: list[str] = []
    next_step: str = ""
    compliance_notes: str = ""


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    hcp_name: str | None = None
    interaction_type: str | None = None
    interaction_datetime: datetime | None = None
    attendees: list[str] | None = None
    topics_discussed: str | None = None
    materials_shared: list[str] | None = None
    samples_distributed: list[str] | None = None
    sentiment: str | None = None
    outcomes: str | None = None
    follow_up_actions: list[str] | None = None
    next_step: str | None = None
    compliance_notes: str | None = None


class InteractionRead(InteractionBase):
    id: int

    model_config = {"from_attributes": True}


class AgentChatRequest(BaseModel):
    user_message: str
    current_form: InteractionBase | None = None


class AgentChatResponse(BaseModel):
    assistant_message: str
    updated_form: dict
    suggested_next_actions: list[str] = []
