import structlog

from configs.db.database import AsyncSessionLocal
from configs.db.enums import NotificationTypeEnum
from configs.db.kafka import get_kafka_consumer, NOTIFICATION_TOPIC
from handlers.notification_handler import NotificationHandler
from repositories.provider.enterprise_follow_user_repository_provider import EnterpriseFollowUserRepositoryProvider
from repositories.provider.follow_repository_provider import FollowRepositoryProvider
from repositories.provider.notification_enterprise_repository_provider import NotificationEnterpriseRepositoryProvider
from repositories.provider.notify_repository_provider import NotifyRepositoryProvider
from schemas.event_notification import EventNotification
from services.provider.enterprise_follow_user_service_provider import EnterpriseFollowUserServiceProvider
from services.provider.follow_service_provider import FollowServiceProvider
from services.provider.notification_enterprise_service_provider import NotificationEnterpriseServiceProvider
from services.provider.notification_service_provider import NotificationServiceProvider

logger = structlog.get_logger()

async def consumer_notification():
    consumer = await get_kafka_consumer(NOTIFICATION_TOPIC, group_id="email-service")

    try :
        async for msg in consumer:
            async with AsyncSessionLocal() as db:
                notify_repository = NotifyRepositoryProvider(db)
                notification_service = NotificationServiceProvider(notify_repository)

                notify_enterprise_repository = NotificationEnterpriseRepositoryProvider(db)
                notification_enterprise_service = NotificationEnterpriseServiceProvider(notify_enterprise_repository)

                follow_repository = FollowRepositoryProvider(db)
                follow_service = FollowServiceProvider(follow_repository)

                enterprise_follow_user_repository = EnterpriseFollowUserRepositoryProvider(db)
                enterprise_follow_user_service = EnterpriseFollowUserServiceProvider(enterprise_follow_user_repository)

                try:
                    event = EventNotification.model_validate_json(msg.value.decode("utf-8"))
                    handler = NotificationHandler(event,
                          follow_service=follow_service,
                          notification_service=notification_service,
                          notification_enterprise_service=notification_enterprise_service,
                          enterprise_follow_service=enterprise_follow_user_service,
                    )

                    if event.event_type == NotificationTypeEnum.NEW_POST:
                        await handler.notify_user_about_new_post()

                    if event.event_type == NotificationTypeEnum.NEW_COMMENT:
                        await handler.notify_user_about_new_comment()

                    if event.event_type == NotificationTypeEnum.NEW_FOLLOWER:
                        await handler.notify_about_new_follow()

                    if event.event_type == NotificationTypeEnum.NEW_POST_ENTERPRISE:
                        await handler.notify_about_new_post_enterprise()

                    if event.event_type == NotificationTypeEnum.NEW_VACANCY:
                        logger.info(f"Event received: {event.model_dump_json()}")
                        await handler.notify_about_new_vacancy()

                    if event.event_type == NotificationTypeEnum.NEW_REVIEW_ENTERPRISE:
                        await handler.notify_enterprise_about_new_review()

                    if event.event_type == NotificationTypeEnum.APPLICATION_RECEIVED:
                        await handler.notify_enterprise_about_new_app()

                    if event.event_type == NotificationTypeEnum.SYSTEM:
                        await handler.notify_user_about_notification_system()

                except Exception as e:
                    logger.error("Failed to process event", error=str(e), message_value=msg.value.decode("utf-8"))
    finally:
        await consumer.stop()
