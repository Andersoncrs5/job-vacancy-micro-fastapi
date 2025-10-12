from abc import ABC, abstractmethod

from configs.db.database import PostUserMetricEntity
from schemas.event_message_metric_schemas import EventMessageMetric


class PostUserMetricServiceBase(ABC):

    @abstractmethod
    async def save_metric(self, metric: PostUserMetricEntity, event: EventMessageMetric):
        pass

    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        pass