import structlog

from configs.db.database import CommentPostUserMetricEntity
from repositories.provider.comment_post_user_metric_repository_provider import CommentPostUserMetricRepositoryProvider

from schemas.event_message_metric_schemas import EventMessageMetric
from services.provider.comment_post_user_metric_service_base import CommentPostUserMetricServiceBase

logger = structlog.get_logger()

class CommentPostUserMetricServiceProvider(CommentPostUserMetricServiceBase):
    def __init__(self, repository: CommentPostUserMetricRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        return await self.repository.get_by_id(comment_id)

    async def save_metric(self, metric: CommentPostUserMetricEntity, event: EventMessageMetric):
        column_name = event.column
        current_value = getattr(metric, column_name, None)

        if current_value is None:
            logger.error(f"Column {column_name} does not exist on CommentPostUserMetricEntity")
            return

        if event.action == "SUM":
            setattr(metric, column_name, current_value + 1)
        elif event.action == "RED":
            setattr(metric, column_name, max(current_value - 1, 0))

        metric_updated = await self.repository.save(metric)

        logger.info("Metric updated successfully")
        logger.info(f"{column_name} before {current_value} after {getattr(metric_updated, column_name)}")