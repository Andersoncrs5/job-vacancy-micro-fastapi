import structlog

from schemas.event_message_schemas import EventMessageMetric, ColumnUserMetricEnum
from services.provider.user_metric_service_provider import UserMetricServiceProvider

logger = structlog.get_logger()

class UserMetricHandler:
    def __init__(self, event: EventMessageMetric, service: UserMetricServiceProvider):
        self.event = event
        self.service = service

    async def handle(self):

        metric = await self.service.get_by_id(self.event.metric_id)
        await self.service.save_metric(metric, self.event)
