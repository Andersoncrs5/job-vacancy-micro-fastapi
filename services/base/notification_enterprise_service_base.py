from abc import ABC, abstractmethod

from configs.db.database import NotificationEntity, FollowerRelationshipEntity, EnterpriseFollowsUserEntity
from schemas.event_notification import EventNotification


class NotificationEnterpriseServiceBase(ABC):
    pass