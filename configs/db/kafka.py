import os
from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")

SUM_RED_METRIC_TOPIC = "sum_red_metric_topic"

async def get_kafka_consumer(topic: str, group_id: str):
    if KAFKA_BOOTSTRAP_SERVERS is None:
        raise ValueError("KAFKA_BOOTSTRAP_SERVERS is None")

    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    return consumer

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    return producer