from typing import TypeVar, Generic, Type, Final

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import Base

T_Entity = TypeVar("T_Entity")
T_Filter = TypeVar("T_Filter")
T_PK = TypeVar("T_PK", bound=int)
T_Model = TypeVar("T_Model", bound=Base)

class GenericRepository(Generic[T_Entity, T_Filter, T_PK, T_Model]):
    def __init__(self, db: AsyncSession, entity_class: Type[T_Model]):
        self.db = db
        self._entity_class = entity_class

    async def add_all(self, entities: list[T_Entity]):
        self.db.add_all(entities)
        await self.db.commit()

    async def save(self, entity: T_Entity) -> T_Entity:
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def save_all(self, entities: list[T_Entity]) -> list[T_Entity]:
        if not entities:
            return []

        await self.db.commit()

        for entity in entities:
            await self.db.refresh(entity)

        return entities

    async def add(self, entity: T_Entity) -> T_Entity:
        self.db.add(entity)

        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: T_Entity):
        await self.db.delete(entity)
        await self.db.commit()

    async def get_by_id(self, _id: T_PK) -> T_Entity | None:
        stmt = select(self._entity_class).where(self._entity_class.id == _id)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def exists_by_id(self, _id: T_PK) -> bool:
        stmt = select(func.count(self._entity_class.id)).where(
            self._entity_class.id == _id
        )

        result: Final[int | None] = await self.db.scalar(stmt)

        return bool(result and result > 0)

    async def get_all(self, _filter: T_Filter) -> list[T_Entity]:
        stmt = _filter.filter(select(self._entity_class))

        result: Final = await self.db.execute(stmt)
        all_entities: Final = result.scalars().all()
        return list(all_entities)