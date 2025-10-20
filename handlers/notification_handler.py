from configs.db.database import FollowerRelationshipEntity, EnterpriseFollowsUserEntity
from schemas.event_notification import EventNotification
from services.provider.enterprise_follow_user_service_provider import EnterpriseFollowUserServiceProvider
from services.provider.follow_service_provider import FollowServiceProvider
from services.provider.notification_service_provider import NotificationServiceProvider


class NotificationHandler:
    def __init__(self,
                 event: EventNotification,
                 follow_service: FollowServiceProvider,
                 notification_service: NotificationServiceProvider,
                 enterprise_follow_service: EnterpriseFollowUserServiceProvider,
                 ):
        self.enterprise_follow_service = enterprise_follow_service
        self.event = event
        self.follow_service = follow_service
        self.notification_service = notification_service

    async def notify_about_new_follow(self):
        await self.notification_service.notify_about_new_follow(event=self.event)

    async def notify_user_about_new_post(self):
        follows: list[FollowerRelationshipEntity] = await self.follow_service.get_all(
            followed_id=self.event.actor_id,
            receive_post=True
        )

        await self.notification_service.notify_users_by_event_follow(follows, event=self.event)

    async def notify_user_about_new_comment(self):
        follows: list[FollowerRelationshipEntity] = await self.follow_service.get_all(
            followed_id=self.event.actor_id,
            receive_comment=True
        )

        await self.notification_service.notify_users_by_event_follow(follows, event=self.event)

    async def notify_about_new_post_enterprise(self):
        follows: list[EnterpriseFollowsUserEntity] = await self.enterprise_follow_service.get_all(
            enterprise_id=self.event.actor_id,
            receive_post=True,
            user_id=None,
            receive_comment=None,
            receive_vacancy = None
        )

        await self.notification_service.notify_users_by_event_follow_by_enterprise(follows, self.event)


    async def notify_about_new_vacancy(self):
        follows: list[EnterpriseFollowsUserEntity] = await self.enterprise_follow_service.get_all(
            enterprise_id=self.event.actor_id,
            receive_post=None,
            user_id=None,
            receive_comment=None,
            receive_vacancy = True
        )

        await self.notification_service.notify_users_by_event_follow_by_enterprise(follows, self.event)
