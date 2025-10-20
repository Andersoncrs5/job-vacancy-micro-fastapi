from abc import ABC, abstractmethod

from configs.db.database import NotificationEntity


class NotifyRepositoryBase(ABC):

    @abstractmethod
    async def save(self, noti: NotificationEntity) -> NotificationEntity:
        pass

    @abstractmethod
    async def add_all(self, noti: list[NotificationEntity]):
        pass

    @abstractmethod
    async def add(self, noti: NotificationEntity) -> NotificationEntity:
        pass

    @abstractmethod
    async def get_by_id(self, _id) -> NotificationEntity | None:
        pass

