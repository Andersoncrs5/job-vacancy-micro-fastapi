from abc import ABC, abstractmethod

from configs.db.database import NotificationEntity, FollowerRelationshipEntity, EnterpriseFollowsUserEntity
from schemas.event_notification import EventNotification


class NotificationServiceBase(ABC):

    @abstractmethod
    async def notify_users_by_event_follow_by_enterprise(self,
                                                         follows: list[EnterpriseFollowsUserEntity],
                                                         event: EventNotification
                                                         ):
        pass

    @abstractmethod
    async def notify_about_new_follow(self, event: EventNotification):
        pass

    @abstractmethod
    async def notify_users_by_event_follow(self,
                                           follows: list[FollowerRelationshipEntity],
                                           event: EventNotification
                                           ):
        pass

    @abstractmethod
    async def get_by_id(self, _id) -> NotificationEntity | None:
        pass