from abc import ABC, abstractmethod

from configs.db.database import CommentPostEnterpriseMetricEntity


class CommentPostEnterpriseMetricRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostEnterpriseMetricEntity:
        pass

    @abstractmethod
    async def save(self, metric: CommentPostEnterpriseMetricEntity) -> CommentPostEnterpriseMetricEntity:
        pass