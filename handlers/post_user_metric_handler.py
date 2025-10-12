import structlog

from schemas.event_message_metric_schemas import EventMessageMetric
from services.provider.post_user_metric_service_provider import PostUserMetricServiceProvider

logger = structlog.get_logger()

class PostUserMetricHandler:
    def __init__(self, event: EventMessageMetric, service: PostUserMetricServiceProvider):
        self.event = event
        self.service = service

    async def handle(self):
        metric = await self.service.get_by_id(self.event.metric_id)
        await self.service.save_metric(metric, self.event)