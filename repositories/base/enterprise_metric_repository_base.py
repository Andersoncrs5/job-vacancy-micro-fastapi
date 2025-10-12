from abc import ABC, abstractmethod

from configs.db.database import EnterpriseMetricEntity


class EnterpriseMetricRepositoryBase(ABC):

    @abstractmethod
    async def save(self, metric: EnterpriseMetricEntity) -> EnterpriseMetricEntity:
        pass

    @abstractmethod
    async def update_metric_value(self, enterprise_id: int, column_name: str, action: str) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, enterprise_id: int) -> EnterpriseMetricEntity:
        pass