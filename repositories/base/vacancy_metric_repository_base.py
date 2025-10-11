from abc import ABC, abstractmethod

from configs.db.database import VacancyMetricEntity


class VacancyMetricRepositoryBase(ABC):

    @abstractmethod
    async def get_by_id(self, vacancy_id: int) -> VacancyMetricEntity:
        pass

    @abstractmethod
    async def save(self, metric: VacancyMetricEntity) -> VacancyMetricEntity:
        pass