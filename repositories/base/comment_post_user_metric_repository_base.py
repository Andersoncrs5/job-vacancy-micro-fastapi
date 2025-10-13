from abc import ABC, abstractmethod

from configs.db.database import CommentPostEnterpriseMetricEntity, CommentPostUserMetricEntity


class CommentPostUserMetricRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentPostUserMetricEntity:
        pass

    @abstractmethod
    async def save(self, metric: CommentPostUserMetricEntity) -> CommentPostUserMetricEntity:
        pass