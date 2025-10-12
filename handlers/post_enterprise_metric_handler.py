import structlog

from schemas.event_message_metric_schemas import EventMessageMetric, ColumnUserMetricEnum
from services.provider.post_enterprise_metric_service_provider import PostEnterpriseMetricServiceProvider

logger = structlog.get_logger()

class PostEnterpriseMetricHandler:
    def __init__(self, event: EventMessageMetric, service: PostEnterpriseMetricServiceProvider):
        self.event = event
        self.service = service

    async def handle(self):
        metric = await self.service.get_by_id(self.event.metric_id)
        await self.service.save_metric(metric, self.event)