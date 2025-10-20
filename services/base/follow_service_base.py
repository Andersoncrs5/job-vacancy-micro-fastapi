from abc import ABC, abstractmethod

from configs.db.database import FollowerRelationshipEntity


class FollowServiceBase(ABC):

    @abstractmethod
    async def get_all(self,
        follower_id: int | None = None,
        followed_id: int | None = None,
        receive_post: bool | None = None,
        receive_comment: bool | None = None,
    ) -> list[FollowerRelationshipEntity]:
        pass