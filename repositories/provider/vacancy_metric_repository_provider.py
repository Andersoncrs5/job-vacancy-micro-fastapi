from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import VacancyMetricEntity
from repositories.base.vacancy_metric_repository_base import VacancyMetricRepositoryBase


class VacancyMetricRepositoryProvider(VacancyMetricRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, metric: VacancyMetricEntity) -> VacancyMetricEntity:
        await self.db.commit()
        await self.db.refresh(metric)

        return metric

    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        stmt = select(VacancyMetricEntity).where(
            VacancyMetricEntity.vacancy_id == vacancy_id
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("Metric not found")

        return metric