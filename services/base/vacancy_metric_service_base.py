from abc import ABC, abstractmethod

from configs.db.database import VacancyMetricEntity
from schemas.event_message_metric_schemas import EventMessageMetric


class VacancyMetricServiceBase(ABC):

    @abstractmethod
    async def save_metric(self, metric: VacancyMetricEntity, event: EventMessageMetric):
        pass

    @abstractmethod
    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        pass

