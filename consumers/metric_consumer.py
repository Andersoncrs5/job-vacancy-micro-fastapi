from typing import Final

import structlog

from configs.db.database import AsyncSessionLocal
from configs.db.kafka import get_kafka_consumer, SUM_RED_METRIC_TOPIC
from handlers.comment_post_enterprise_metric_handler import CommentPostEnterpriseMetricHandler
from handlers.enterprise_metric_handler import EnterpriseMetricHandler
from handlers.post_enterprise_metric_handler import PostEnterpriseMetricHandler
from handlers.post_user_metric_handler import PostUserMetricHandler
from handlers.user_metric_handler import UserMetricHandler
from handlers.vacancy_metric_handler import VacancyMetricHandler
from repositories.provider.comment_post_enterprise_metric_repository_provider import \
    CommentPostEnterpriseMetricRepositoryProvider
from repositories.provider.enterprise_metric_repository_provider import EnterpriseMetricRepositoryProvider
from repositories.provider.post_enterprise_metric_repository_provider import PostEnterpriseMetricRepositoryProvider
from repositories.provider.post_user_metric_repository_provider import PostUserMetricRepositoryProvider
from repositories.provider.user_metric_repository_provider import UserMetricRepositoryProvider
from repositories.provider.vacancy_metric_repository_provider import VacancyMetricRepositoryProvider
from schemas.event_message_metric_schemas import EventMessageMetric, EntityEnum
from services.base.comment_post_enterprise_metric_service_provider import CommentPostEnterpriseMetricServiceProvider
from services.provider.enterprise_metric_service_provider import EnterpriseMetricServiceProvider
from services.provider.post_enterprise_metric_service_provider import PostEnterpriseMetricServiceProvider
from services.provider.post_user_metric_service_provider import PostUserMetricServiceProvider
from services.provider.user_metric_service_provider import UserMetricServiceProvider
from services.provider.vacancy_metric_service_provider import VacancyMetricServiceProvider

logger = structlog.get_logger()

async def consume_metric_events():
    consumer = await get_kafka_consumer(SUM_RED_METRIC_TOPIC, group_id="metric-service")

    try:
        async for msg in consumer:
            async with AsyncSessionLocal() as db:
                repository_metric_user = UserMetricRepositoryProvider(db)
                user_metric_service = UserMetricServiceProvider(repository_metric_user)

                repository_metric_vacancy = VacancyMetricRepositoryProvider(db)
                vacancy_metric_service = VacancyMetricServiceProvider(repository_metric_vacancy)

                repository_metric_enterprise = EnterpriseMetricRepositoryProvider(db)
                enterprise_metric_service = EnterpriseMetricServiceProvider(repository_metric_enterprise)

                repository_metric_enterprise_post = PostEnterpriseMetricRepositoryProvider(db)
                post_enterprise_metric_service = PostEnterpriseMetricServiceProvider(repository_metric_enterprise_post)

                repository_metric_user_post = PostUserMetricRepositoryProvider(db)
                post_user_metric_service = PostUserMetricServiceProvider(repository_metric_user_post)

                repository_metric_comment_post_enterprise = CommentPostEnterpriseMetricRepositoryProvider(db)
                comment_post_enterprise_metric_service = CommentPostEnterpriseMetricServiceProvider(repository_metric_comment_post_enterprise)

                try:
                    event = EventMessageMetric.model_validate_json(msg.value.decode("utf-8"))
                    logger.info(f"Event received: {event.model_dump_json()}")

                    if event.entity == EntityEnum.USER_METRIC:
                        handler = UserMetricHandler(event, user_metric_service)
                        await handler.handle()

                    elif event.entity == EntityEnum.VACANCY_METRIC:
                        handler = VacancyMetricHandler(event, vacancy_metric_service)
                        await handler.handle()

                    elif event.entity == EntityEnum.ENTERPRISE_METRIC:
                        handler = EnterpriseMetricHandler(event, enterprise_metric_service)
                        await handler.handle()

                    elif event.entity == EntityEnum.POST_ENTERPRISE_METRIC:
                        handler = PostEnterpriseMetricHandler(event, post_enterprise_metric_service)
                        await handler.handle()

                    elif event.entity == EntityEnum.POST_USER_METRIC:
                        handler = PostUserMetricHandler(event, post_user_metric_service)
                        await handler.handle()

                    elif event.entity == EntityEnum.COMMENT_POST_ENTERPRISE_METRIC:
                        handler = CommentPostEnterpriseMetricHandler(event, comment_post_enterprise_metric_service)
                        await handler.handle()

                except Exception as e:
                    logger.error("Failed to process event", error=str(e), message_value=msg.value.decode("utf-8"))
    finally:
        await consumer.stop()