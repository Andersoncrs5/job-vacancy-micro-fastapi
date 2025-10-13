from configs.db.database import UserEntity
from repositories.provider.user_repository_provider import UserRepositoryProvider
from services.base.user_service_base import UserServiceBase


class UserServiceProvider(UserServiceBase):
    def __init__(self, repository: UserRepositoryProvider):
        self.repository = repository

    async def get_by_email(self, email: str) -> UserEntity:
        return await self.repository.get_by_email(email)