import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LearningRecord, KnowledgeNode, LearningPath
from app.repositories.base import BaseRepository


class LearningRecordRepository(BaseRepository):
    def __init__(self):
        super().__init__(LearningRecord)

    async def get_by_student(self, db: AsyncSession, student_id: uuid.UUID) -> list[LearningRecord]:
        result = await db.execute(
            select(LearningRecord).where(LearningRecord.student_id == student_id)
        )
        return list(result.scalars().all())

    async def get_student_knowledge_status(self, db: AsyncSession, student_id: uuid.UUID) -> list[tuple[LearningRecord, KnowledgeNode]]:
        result = await db.execute(
            select(LearningRecord, KnowledgeNode)
            .join(KnowledgeNode, LearningRecord.knowledge_node_id == KnowledgeNode.id)
            .where(LearningRecord.student_id == student_id)
        )
        return list(result.all())

class LearningPathRepository(BaseRepository):
    def __init__(self):
        super().__init__(LearningPath)

    async def get_by_student(self, db: AsyncSession, student_id: uuid.UUID) -> list[LearningPath]:
        result = await db.execute(
            select(LearningPath).where(LearningPath.student_id == student_id)
        )
        return list(result.scalars().all())

learning_record_repo = LearningRecordRepository()
learning_path_repo = LearningPathRepository()