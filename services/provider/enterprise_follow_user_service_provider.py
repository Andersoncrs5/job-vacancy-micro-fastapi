from repositories.provider.enterprise_follow_user_repository_provider import EnterpriseFollowUserRepositoryProvider
from services.base.enterprise_follow_user_service_base import EnterpriseFollowUserServiceBase


class EnterpriseFollowUserServiceProvider(EnterpriseFollowUserServiceBase):
    def __init__(self, repository: EnterpriseFollowUserRepositoryProvider):
        self.repository = repository

    async def get_all(self,
                      enterprise_id: int | None,
                      user_id: int | None,
                      receive_post: bool | None,
                      receive_comment: bool | None,
                      receive_vacancy: bool | None,
                      ):
        return await self.repository.get_all(
            enterprise_id=enterprise_id,
            user_id=user_id,
            receive_post=receive_post,
            receive_comment=receive_comment,
            receive_vacancy=receive_vacancy,
        )

