import structlog

from configs.db.database import PostUserMetricEntity
from repositories.provider.post_user_metric_repository_provider import PostUserMetricRepositoryProvider
from schemas.event_message_metric_schemas import EventMessageMetric
from services.base.post_user_metric_service_base import PostUserMetricServiceBase

logger = structlog.get_logger()

class PostUserMetricServiceProvider(PostUserMetricServiceBase):
    def __init__(self, repository: PostUserMetricRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        return await self.repository.get_by_id(post_id)

    async def save_metric(self, metric: PostUserMetricEntity, event: EventMessageMetric):
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

        logger.info("Post User Metric updated successfully")
        logger.info(f"{column_name} before {current_value} after {getattr(metric_updated, column_name)}")