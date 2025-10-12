from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import PostUserMetricEntity
from repositories.base.post_user_metric_repository_base import PostUserMetricRepositoryBase

class PostUserMetricRepositoryProvider(PostUserMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        stmt = select(PostUserMetricEntity).where(
            PostUserMetricEntity.post_id == post_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric not found")

        return metric

    async def save(self, metric: PostUserMetricEntity) -> PostUserMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric