import structlog

from configs.db.database import AsyncSessionLocal
from configs.db.kafka import get_kafka_consumer, SUM_RED_METRIC_TOPIC
from handlers.user_metric_handler import UserMetricHandler
from handlers.vacancy_metric_handler import VacancyMetricHandler
from repositories.provider.user_metric_repository_provider import UserMetricRepositoryProvider
from repositories.provider.vacancy_metric_repository_provider import VacancyMetricRepositoryProvider
from schemas.event_message_metric_schemas import EventMessageMetric, EntityEnum
from services.provider.user_metric_service_provider import UserMetricServiceProvider
from services.provider.vacancy_metric_service_provider import VacancyMetricServiceProvider

logger = structlog.get_logger()

async def consume_metric_events():
    consumer = await get_kafka_consumer(SUM_RED_METRIC_TOPIC, group_id="metric-service")

    async with AsyncSessionLocal() as db:
        repository_metric_user = UserMetricRepositoryProvider(db)
        user_metric_service = UserMetricServiceProvider(repository_metric_user)

        repository_metric_vacancy = VacancyMetricRepositoryProvider(db)
        vacancy_metric_service = VacancyMetricServiceProvider(repository_metric_vacancy)

        try:
            async for msg in consumer:
                try:
                    event = EventMessageMetric.model_validate_json(msg.value.decode("utf-8"))
                    logger.info(f"Event received: {event.json()}")

                    if event.entity == EntityEnum.USER_METRIC:
                        handler = UserMetricHandler(event, user_metric_service)
                        await handler.handle()

                    if event.entity == EntityEnum.VACANCY_METRIC:
                        handler = VacancyMetricHandler(event, vacancy_metric_service)
                        await handler.handle()

                except Exception as e:
                    logger.error("Failed to process event", error=str(e))
        finally:
            await consumer.stop()