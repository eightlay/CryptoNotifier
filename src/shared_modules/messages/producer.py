import os
import json
from aiokafka import AIOKafkaProducer


async def get_producer() -> AIOKafkaProducer:
    producer = AIOKafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", ":9092"),
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )
    await producer.start()
    return producer
