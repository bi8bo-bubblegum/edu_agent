import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LearningRecord(Base):
    __tablename__ = "learning_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    knowledge_node_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    mastery_level: Mapped[str] = mapped_column(String(20), default="not_started")
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    time_spent_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    student: Mapped["User"] = relationship(
        back_populates="learning_records",
        primaryjoin="LearningRecord.student_id == User.id",
        foreign_keys=[student_id]
    )

    knowledge_node: Mapped["KnowledgeNode"] = relationship(
        back_populates="learning_records",
        primaryjoin="LearningRecord.knowledge_node_id == KnowledgeNode.id",
        foreign_keys=[knowledge_node_id]
    )


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    target_subject: Mapped[str] = mapped_column(String(100), nullable=False)
    node_sequence: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of UUID list
    current_index: Mapped[int] = mapped_column(Integer, default=0)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())