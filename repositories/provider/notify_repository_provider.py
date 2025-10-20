import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import NotificationEntity
from repositories.base.notify_repository_base import NotifyRepositoryBase

logger = structlog.get_logger()

class NotifyRepositoryProvider(NotifyRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, noti: NotificationEntity) -> NotificationEntity:
        await self.db.commit()
        await self.db.refresh(noti)

        return noti

    async def add(self, noti: NotificationEntity) -> NotificationEntity:
        self.db.add(noti)
        await self.db.commit()
        await self.db.refresh(noti)

        return noti

    async def add_all(self, noti: list[NotificationEntity]):
        self.db.add_all(noti)
        await self.db.commit()

        log_data = [
            {"id": n.id, "user_id": n.user_id, "type": n.type.name}
            for n in noti
        ]

        logger.info("Notifications added successfully", count=len(noti), notifications=log_data)

    async def get_by_id(self, _id) -> NotificationEntity | None:
        stmt = select(NotificationEntity).where(
            NotificationEntity.id == _id
        )

        data = await self.db.execute(stmt)

        return data.scalars().first()