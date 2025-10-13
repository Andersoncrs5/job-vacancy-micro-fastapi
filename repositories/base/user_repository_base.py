from abc import ABC, abstractmethod

from configs.db.database import UserEntity


class UserRepositoryBase(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity:
        pass