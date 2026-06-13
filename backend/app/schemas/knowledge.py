import uuid
from datetime import datetime

from pydantic import BaseModel


class KnowledgeNodeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    subject: str
    chapter: str
    difficulty: int
    created_at: datetime

    model_config = {"from_attributes": True}


class KnowledgeGraphEdge(BaseModel):
    source_id: uuid.UUID
    target_id: uuid.UUID
    relation: str  # "prerequisite"


class KnowledgeGraphResponse(BaseModel):
    nodes: list[KnowledgeNodeResponse]
    edges: list[KnowledgeGraphEdge]


class KnowledgeStatusResponse(BaseModel):
    knowledge_node_id: uuid.UUID
    name: str
    mastery_level: str
    score: float | None