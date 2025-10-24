from configs.db.database import NotificationEnterpriseEntity
from configs.db.enums import NotificationTypeEnum
from repositories.provider.notification_enterprise_repository_provider import NotificationEnterpriseRepositoryProvider
from schemas.event_notification import EventNotification
from services.base.notification_enterprise_service_base import NotificationEnterpriseServiceBase


class NotificationEnterpriseServiceProvider(NotificationEnterpriseServiceBase):
    def __init__(self, repository: NotificationEnterpriseRepositoryProvider):
        self.repository = repository

    async def create_notify(self, event: EventNotification):
        actor_name = event.data.get("actor_name", None)
        vacancy_name = event.data.get("vacancy_name", None)

        title_dynamic = ""
        content_dynamic = ""

        if event.event_type == NotificationTypeEnum.NEW_REVIEW_ENTERPRISE:
            title_dynamic = "New Review Received!"
            content_dynamic = f"{actor_name} just left a new review! View the details and respond quickly."

        if event.event_type == NotificationTypeEnum.NEW_REVIEW_ENTERPRISE:
            title_dynamic = "New Application Received!"
            content_dynamic = f"{actor_name} just applied to your vacancy: {vacancy_name}. Review their profile now!"

        notify = NotificationEnterpriseEntity(
            enterprise_id = event.actor_id,
            title = title_dynamic,
            content = content_dynamic,
            link = None,
            type = event.event_type,
            entity_id = event.entity_id
        )

        await self.repository.add(notify)