from configs.db.database import NotificationEntity, FollowerRelationshipEntity, UserEntity, EnterpriseFollowsUserEntity
from configs.db.enums import NotificationTypeEnum
from repositories.provider.notify_repository_provider import NotifyRepositoryProvider
from schemas.event_notification import EventNotification
from services.base.notification_service_base import NotificationServiceBase


class NotificationServiceProvider(NotificationServiceBase):
    def __init__(self, repository: NotifyRepositoryProvider):
        self.repository = repository

    async def get_by_id(self, _id) -> NotificationEntity | None:
        return await self.repository.get_by_id(_id)

    async def notify_about_new_follow(self, event: EventNotification):
        user_name = event.data.get("user_name", None)
        notify = NotificationEntity(
            user_id=event.entity_id,
            title=f"{user_name} started following you!",
            content="You have a new follower.",
            link=None,
            type=event.event_type,
            entity_id=event.actor_id
        )

        await self.repository.add(notify)

    async def notify_users_by_event_follow(self,
                                    follows: list[FollowerRelationshipEntity],
                                    event: EventNotification
                                    ):

        notifies = []
        title = ""
        content = ""

        user_name = event.data.get("user_name", None)
        actor_name = event.data.get("actor_name", None)

        for follow in follows:

            if event.event_type == NotificationTypeEnum.NEW_COMMENT:
                title = f"The user {user_name} created a new comment!"
                content = f"The user you follow, {user_name}, just created a new comment!"

            if event.event_type == NotificationTypeEnum.NEW_POST:
                title = f"The user {user_name} created a new post!"
                content = f"The user you follow, {user_name}, just created a new post!"

            recipient_user_id = follow.follower_id

            notify = NotificationEntity(
                user_id=recipient_user_id,
                title=title,
                content=content,
                link=None,
                type=event.event_type,
                entity_id=event.entity_id
            )

            notifies.append(notify)

        await self.repository.add_all(notifies)

    async def notify_users_by_event_follow_by_enterprise(self,
                                    follows: list[EnterpriseFollowsUserEntity],
                                    event: EventNotification
                                    ):

        notifies = []
        title = ""
        content = ""

        actor_name = event.data.get("actor_name", None)

        for follow in follows:

            if event.event_type == NotificationTypeEnum.NEW_POST_ENTERPRISE:
                title = f"The enterprise {actor_name} created a new post!"
                content = f"The enterprise you follow, {actor_name}, just created a new post!"

            if event.event_type == NotificationTypeEnum.NEW_VACANCY:
                title = f"The enterprise {actor_name} created a new vacancy!"
                content = f"The enterprise you follow, {actor_name}, just created a new vacancy!"

            notify = NotificationEntity(
                user_id=follow.user_id,
                title=title,
                content=content,
                link=None,
                type=event.event_type,
                entity_id=event.entity_id
            )

            notifies.append(notify)

        await self.repository.add_all(notifies)