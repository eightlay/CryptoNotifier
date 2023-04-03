import os
import json
from aiokafka import AIOKafkaConsumer


async def get_consumer(topic: str) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", ":9092"),
        group_id='tg',
        value_deserializer=lambda m: json.loads(m)
    )
    await consumer.start()
    return consumer
