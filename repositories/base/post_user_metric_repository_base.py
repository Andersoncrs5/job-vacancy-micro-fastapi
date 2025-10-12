from abc import ABC, abstractmethod

from configs.db.database import PostUserMetricEntity


class PostUserMetricRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostUserMetricEntity:
        pass

    @abstractmethod
    async def save(self, metric: PostUserMetricEntity) -> PostUserMetricEntity:
        pass