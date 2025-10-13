from abc import abstractmethod, ABC

from configs.db.database import CommentPostEnterpriseMetricEntity, CommentPostUserMetricEntity
from schemas.event_message_metric_schemas import EventMessageMetric


class CommentPostUserMetricServiceBase(ABC):

    @abstractmethod
    async def save_metric(self, metric: CommentPostUserMetricEntity, event: EventMessageMetric):
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        pass