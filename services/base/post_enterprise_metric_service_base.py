from abc import ABC, abstractmethod

from configs.db.database import PostEnterpriseMetricEntity
from schemas.event_message_metric_schemas import EventMessageMetric


class PostEnterpriseMetricServiceBase(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def save_metric(self, metric: PostEnterpriseMetricEntity, event: EventMessageMetric):
        pass
