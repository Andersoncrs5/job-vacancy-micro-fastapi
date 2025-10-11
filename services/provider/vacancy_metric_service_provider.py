import structlog

from configs.db.database import VacancyMetricEntity
from repositories.provider.vacancy_metric_repository_provider import VacancyMetricRepositoryProvider
from schemas.event_message_metric_schemas import EventMessageMetric
from services.base.vacancy_metric_service_base import VacancyMetricServiceBase

logger = structlog.get_logger()

class VacancyMetricServiceProvider(VacancyMetricServiceBase):
    def __init__(self, repository: VacancyMetricRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        return await self.repository.get_by_id(vacancy_id)

    async def save_metric(self, metric: VacancyMetricEntity, event: EventMessageMetric):
        column_name = event.column
        current_value = getattr(metric, column_name, None)

        if current_value is None:
            logger.error(f"Column {column_name} does not exist on VacancyMetricEntity")
            return

        if event.action == "SUM":
            setattr(metric, column_name, current_value + 1)
        elif event.action == "RED":
            setattr(metric, column_name, max(current_value - 1, 0))

        metric_updated = await self.repository.save(metric)

        logger.info("Metric updated successfully")
        logger.info(f"{column_name} before {current_value} after {getattr(metric_updated, column_name)}")