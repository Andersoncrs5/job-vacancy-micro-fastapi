from abc import ABC, abstractmethod

from configs.db.database import UserMetricEntity


class UserMetricRepositoryBase(ABC):

    @abstractmethod
    async def save(self, metric: UserMetricEntity) -> UserMetricEntity:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserMetricEntity:
        pass