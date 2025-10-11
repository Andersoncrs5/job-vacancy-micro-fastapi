import structlog

from configs.db.database import UserMetricEntity
from repositories.provider.user_metric_repository_provider import UserMetricRepositoryProvider
from schemas.event_message_metric_schemas import SumRedEnum, EventMessageMetric
from services.base.user_metric_service_base import UserMetricServiceBase

logger = structlog.get_logger()

class UserMetricServiceProvider(UserMetricServiceBase):
    def __init__(self, repository: UserMetricRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, user_id: int) -> UserMetricEntity:
        return await self.repository.get_by_id(user_id)

    async def post_count_sum_red(self, metric: UserMetricEntity, action: SumRedEnum) -> UserMetricEntity:
        if action == SumRedEnum.SUM:
            metric.post_count += 1

        if action == SumRedEnum.RED:
            metric.post_count = max(metric.post_count - 1, 0)

        return await self.repository.save(metric)

    async def save_metric(self, metric: UserMetricEntity, event: EventMessageMetric):
        column_name = event.column
        current_value = getattr(metric, column_name, None)

        if current_value is None:
            logger.error(f"Column {column_name} does not exist on UserMetricEntity")
            return

        if event.action == "SUM":
            setattr(metric, column_name, current_value + 1)
        elif event.action == "RED":
            setattr(metric, column_name, max(current_value - 1, 0))

        metric_updated = await self.repository.save(metric)

        logger.info("Metric updated successfully")
        logger.info(f"{column_name} before {current_value} after {getattr(metric_updated, column_name)}")