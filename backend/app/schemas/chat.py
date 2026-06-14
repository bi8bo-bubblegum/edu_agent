import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ChatSessionCreate(BaseModel):
    knowledge_node_id: uuid.UUID | None = None
    title: str | None = None

class ChatSessionResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    knowledge_node_id: uuid.UUID | None
    active_agent: str
    title: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    role: str
    content: str
    agent_name: str | None
    created_at: datetime

    model_config = {"from_attributes": True}