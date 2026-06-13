import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatSession, ChatMessage
from app.repositories.base import BaseRepository


class ChatSessionRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatSession)

    async def get_user_session(self, db: AsyncSession, student_id: uuid.UUID) -> list[ChatSession]:
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.student_id == student_id)
            .order_by(ChatSession.created_at.desc())
        )
        return list(result.scalars().all())

class ChatMessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatMessage)

    async def get_session_messages(self, db: AsyncSession, session_id: uuid.UUID) -> list[ChatMessage]:
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at)
        )
        return list(result.scalars().all())

chat_session_repo = ChatSessionRepository()
chat_message_repo = ChatMessageRepository()