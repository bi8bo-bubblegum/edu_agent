from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KnowledgeNode
from app.repositories.base import BaseRepository


class KnowledgeRepository(BaseRepository):
    def __init__(self):
        super().__init__(KnowledgeNode)

    async def get_by_subject(self, db: AsyncSession, subject: str) -> list[KnowledgeNode]:
        result = await db.execute(
            select(KnowledgeNode).where(KnowledgeNode.subject == subject)
        )
        return list(result.scalars().all())

knowledge_repo = KnowledgeRepository()