import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MasteryLevel(str, Enum):
    NOT_STARTED = "not_started"
    LEARNING = "learning"
    MASTERED = "mastered"
    NEEDS_REVIEW = "needs_review"

class LearningRecordResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    knowledge_node_id: uuid.UUID
    mastery_level: str
    score: float | None
    time_spend_minutes: int | None
    created_at: datetime

    model_config = {"from_attributes": True}

class LearningPathResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    target_subject: str
    node_sequence: list[uuid.UUID]
    current_index: int
    rationale: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class LearningPathGenerateRequest(BaseModel):
    target_subject: str
    target_knowledge_node_id: uuid.UUID | None = None


class LearningProgressUpdate(BaseModel):
    knowledge_node_id: uuid.UUID
    mastery_level: MasteryLevel
    score: float | None = None
    time_spent_minutes: int | None = None
