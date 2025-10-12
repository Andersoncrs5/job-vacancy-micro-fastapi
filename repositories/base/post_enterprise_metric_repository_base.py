from abc import ABC, abstractmethod

from configs.db.database import PostEnterpriseMetricEntity


class PostEnterpriseMetricRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> PostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def save(self, metric: PostEnterpriseMetricEntity) -> PostEnterpriseMetricEntity:
        pass