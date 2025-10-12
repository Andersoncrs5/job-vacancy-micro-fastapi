from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import CommentPostEnterpriseMetricEntity
from repositories.base.comment_post_enterprise_metric_repository_base import CommentPostEnterpriseMetricRepositoryBase


class CommentPostEnterpriseMetricRepositoryProvider(CommentPostEnterpriseMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        stmt = select(CommentPostEnterpriseMetricEntity).where(
            CommentPostEnterpriseMetricEntity.comment_id == comment_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric not found")

        return metric

    async def save(self, metric: CommentPostEnterpriseMetricEntity) -> CommentPostEnterpriseMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric