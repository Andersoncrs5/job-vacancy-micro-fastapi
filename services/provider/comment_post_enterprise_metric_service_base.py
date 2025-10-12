from abc import abstractmethod, ABC

from configs.db.database import CommentPostEnterpriseMetricEntity
from schemas.event_message_metric_schemas import EventMessageMetric


class CommentPostEnterpriseMetricServiceBase(ABC):

    @abstractmethod
    async def save_metric(self, metric: CommentPostEnterpriseMetricEntity, event: EventMessageMetric):
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        pass