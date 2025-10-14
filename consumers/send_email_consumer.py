import structlog

from configs.db.database import AsyncSessionLocal
from configs.db.kafka import get_kafka_consumer, SEND_EMAIL_TOPIC
from handlers.email_handler import EmailHandler
from repositories.provider.user_repository_provider import UserRepositoryProvider
from schemas.event_message_email import EventMessageEmail
from services.provider.email_service_provider import EmailServiceProvider
from services.provider.user_service_provider import UserServiceProvider
from templates.template_manager import TemplateManager

logger = structlog.get_logger()

async def consume_send_email():
    consumer = await get_kafka_consumer(SEND_EMAIL_TOPIC, group_id="email-service")

    try:
        async for msg in consumer:
            async with AsyncSessionLocal() as db:
                repository_user = UserRepositoryProvider(db)
                user_service = UserServiceProvider(repository_user)

                email_service = EmailServiceProvider()

                template_manager = TemplateManager()

                try:
                    event = EventMessageEmail.model_validate_json(msg.value.decode("utf-8"))
                    logger.info(f"Event received: {event.model_dump_json()}")

                    handler = EmailHandler(event, user_service, email_service, template_manager)
                    await handler.send_email_welcome()

                    await consumer.commit()
                except Exception as e:
                    logger.error("Failed to process event", error=str(e), message_value=msg.value.decode("utf-8"))
    finally:
        await consumer.stop()
