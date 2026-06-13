import uuid
from typing import TypeVar, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository:

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: uuid.UUID) -> ModelType | None:
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, **kwargs: Any) -> ModelType:
        instance = self.model(**kwargs)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def update(self, db: AsyncSession, id: uuid.UUID, **kwargs: Any) -> ModelType | None:
        instance = await self.get_by_id(db, id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def delete(self, db: AsyncSession, id: uuid.UUID) -> bool:
        instance = await self.get_by_id(db, id)
        if instance is None:
            return False
        await db.delete(instance)
        await db.commit()
        return True