from abc import ABC, abstractmethod

from configs.db.database import EnterpriseMetricEntity
from schemas.event_message_metric_schemas import EventMessageMetric, SumRedEnum


class EnterpriseMetricServiceBase(ABC):

    @abstractmethod
    async def update_metric(self, enterprise_id: int, column_name: str, action: SumRedEnum) -> None:
        pass
    @abstractmethod
    async def save_metric(self, metric: EnterpriseMetricEntity, event: EventMessageMetric):
        pass

    @abstractmethod
    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        pass
