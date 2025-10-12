import structlog

from configs.db.database import EnterpriseMetricEntity
from repositories.provider.enterprise_metric_repository_provider import EnterpriseMetricRepositoryProvider
from schemas.event_message_metric_schemas import EventMessageMetric, SumRedEnum
from services.base.enterprise_metric_service_base import EnterpriseMetricServiceBase

logger = structlog.get_logger()

class EnterpriseMetricServiceProvider(EnterpriseMetricServiceBase):
    def __init__(self, repository: EnterpriseMetricRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        return await self.repository.get_by_id(enterprise_id)

    async def update_metric(self, enterprise_id: int, column_name: str, action: SumRedEnum) -> None:
        await self.repository.update_metric_value(enterprise_id, column_name, action)

    async def save_metric(self, metric: EnterpriseMetricEntity, event: EventMessageMetric):
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

        logger.info("Enterprise Metric updated successfully")
        logger.info(f"{column_name} before {current_value} after {getattr(metric_updated, column_name)}")