import structlog

from schemas.event_message_metric_schemas import EventMessageMetric
from services.base.comment_post_enterprise_metric_service_provider import CommentPostEnterpriseMetricServiceProvider

logger = structlog.get_logger()

class CommentPostEnterpriseMetricHandler:
    def __init__(self, event: EventMessageMetric, service: CommentPostEnterpriseMetricServiceProvider):
        self.event = event
        self.service = service

    async def handle(self):
        metric = await self.service.get_by_id(self.event.metric_id)
        await self.service.save_metric(metric, self.event)