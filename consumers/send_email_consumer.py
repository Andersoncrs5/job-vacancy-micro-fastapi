import structlog

from configs.db.kafka import get_kafka_consumer, SEND_EMAIL_TOPIC
from schemas.event_message_email import EventMessageEmail

logger = structlog.get_logger()

async def consume_email():
    consumer = await get_kafka_consumer(SEND_EMAIL_TOPIC, group_id="email-service")

    try:
        async for msg in consumer:
            try:
                event = EventMessageEmail.model_validate_json(msg.value.decode("utf-8"))
                logger.info(f"Event received: {event.model_dump_json()}")

            except Exception as e:
                logger.error("Failed to process event", error=str(e), message_value=msg.value.decode("utf-8"))
    finally:
        await consumer.stop()
