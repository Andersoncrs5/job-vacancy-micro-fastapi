from configs.db.database import FollowerRelationshipEntity
from repositories.provider.follow_repository_provider import FollowRepositoryProvider
from services.base.follow_service_base import FollowServiceBase


class FollowServiceProvider(FollowServiceBase):
    def __init__(self, repository: FollowRepositoryProvider):
        self.repository = repository

    async def get_all(self,
        follower_id: int | None = None,
        followed_id: int | None = None,
        receive_post: bool | None = None,
        receive_comment: bool | None = None,
    ) -> list[FollowerRelationshipEntity]:
        return await self.repository.get_all(
            follower_id=follower_id,
            followed_id=followed_id,
            receive_post=receive_post,
            receive_comment=receive_comment,
        )