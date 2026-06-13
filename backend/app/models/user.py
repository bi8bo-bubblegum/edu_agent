import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    learning_preference: Mapped[str] = mapped_column(String(20), default="guided")
    learning_goal: Mapped[str] = mapped_column(String(20), default="understanding")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())
    learning_records: Mapped[list["LearningRecord"]] = relationship(back_populates="student",
                                                                    foreign_keys="LearningRecord.student_id")
    chat_sessions: Mapped[list["ChatSession"]] = relationship(back_populates="student",
                                                              foreign_keys="ChatSession.student_id")