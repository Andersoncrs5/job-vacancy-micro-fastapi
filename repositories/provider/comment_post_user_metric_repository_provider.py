from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import CommentPostUserMetricEntity
from repositories.base.comment_post_user_metric_repository_base import CommentPostUserMetricRepositoryBase

class CommentPostUserMetricRepositoryProvider(CommentPostUserMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        stmt = select(CommentPostUserMetricEntity).where(
            CommentPostUserMetricEntity.comment_id == comment_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("CommentPostUserMetricEntity not found")

        return metric

    async def save(self, metric: CommentPostUserMetricEntity) -> CommentPostUserMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric