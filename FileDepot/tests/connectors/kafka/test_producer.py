import asyncio
import pytest
from app.connectors.kafka.interface.producer import FastStreamKafkaProducer

BROKERS = ["localhost:9092"]
TOPIC = "test"

@pytest.mark.asyncio
async def test_kafka_producer_send():
    producer = FastStreamKafkaProducer(brokers=BROKERS)
    await producer.broker.start()  # 연결
    message = {"foo": "bar"}
    await producer.send(TOPIC, message)
    await producer.broker.close()  # 연결 해제
    # 별도의 assert는 불필요, 예외 없이 동작하면 성공
    # 실제 메시지 소비는 별도 consumer 테스트에서 검증
