import asyncio
import pytest
from app.connectors.kafka.interface.producer import FastStreamKafkaProducer
from app.connectors.kafka.interface.aiokafka_consumer_impl import AIOKafkaConsumerImpl

BROKERS = ["localhost:9092"]
TOPIC = "test"
GROUP_ID = "test-group"

@pytest.mark.asyncio
async def test_kafka_consumer_receive():
    consumer = AIOKafkaConsumerImpl(brokers=BROKERS, group_id=GROUP_ID)
    producer = FastStreamKafkaProducer(brokers=BROKERS)
    await producer.broker.start()
    await producer.send(TOPIC, {"foo": "bar"})
    await producer.broker.close()
    # kafka에 메시지가 도달할 시간을 약간 기다림
    await asyncio.sleep(1)
    msgs = await consumer.read_messages(TOPIC, limit=1)
    assert msgs[0]["foo"] == "bar"
