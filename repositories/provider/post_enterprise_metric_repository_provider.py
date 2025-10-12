from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import PostEnterpriseMetricEntity
from repositories.base.post_enterprise_metric_repository_base import PostEnterpriseMetricRepositoryBase


class PostEnterpriseMetricRepositoryProvider(PostEnterpriseMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        stmt = select(PostEnterpriseMetricEntity).where(
            PostEnterpriseMetricEntity.post_id == post_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric not found")

        return metric

    async def save(self, metric: PostEnterpriseMetricEntity) -> PostEnterpriseMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric