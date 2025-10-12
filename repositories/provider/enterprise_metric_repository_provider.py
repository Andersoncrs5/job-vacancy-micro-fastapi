from sqlalchemy import select, literal_column, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import EnterpriseMetricEntity
from repositories.base.enterprise_metric_repository_base import EnterpriseMetricRepositoryBase
from schemas.event_message_metric_schemas import SumRedEnum


class EnterpriseMetricRepositoryProvider(EnterpriseMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        stmt = select(EnterpriseMetricEntity).where(
            EnterpriseMetricEntity.enterprise_id == enterprise_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric not found")

        return metric

    async def save(self, metric: EnterpriseMetricEntity) -> EnterpriseMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric

    async def update_metric_value(self, enterprise_id: int, column_name: str, action: SumRedEnum) -> None:
        if action == SumRedEnum.SUM:
            value_expression = literal_column(column_name) + 1
        else:  # RED
            value_expression = func.greatest(0, literal_column(column_name) - 1)

        stmt = (
            update(EnterpriseMetricEntity)
            .where(EnterpriseMetricEntity.enterprise_id == enterprise_id)
            .values({column_name: value_expression})
        )
        await self.db.execute(stmt)
        await self.db.commit()