from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import UserMetricEntity
from repositories.base.user_metric_repository_base import UserMetricRepositoryBase


class UserMetricRepositoryProvider(UserMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> UserMetricEntity:
        stmt = select(UserMetricEntity).where(
            UserMetricEntity.user_id == user_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric not found")

        return metric

    async def save(self, metric: UserMetricEntity) -> UserMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric