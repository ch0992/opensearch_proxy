import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.connectors.kafka.interface.aiokafka_consumer_impl import AIOKafkaConsumerImpl
from app.connectors.kafka.interface.producer import FastStreamKafkaProducer

BROKERS = ["localhost:9092"]
GROUP_ID = "test-api-consume"

@pytest.mark.asyncio
async def test_api_kafka_base64(tmp_path):
    # 1. consumer 준비 (테스트용)
    consumer = AIOKafkaConsumerImpl(brokers=BROKERS, group_id=GROUP_ID)
    producer = FastStreamKafkaProducer(brokers=BROKERS)
    await producer.broker.start()
    # 파일 업로드 후 메시지가 Kafka에 도달할 시간을 약간 기다림
    await asyncio.sleep(1)

    # 2. httpx로 API에 파일 업로드 요청 (ASGITransport 사용)
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 샘플 바이너리 파일 생성
        sample_file = tmp_path / "test.jpg"
        sample_file.write_bytes(b"testdata1234")
        with sample_file.open("rb") as f:
            files = {"file": ("test.jpg", f, "image/jpeg")}
            resp = await ac.post("/api/v1/kafka/upload-base64", files=files)
            assert resp.status_code == 200

    # 3. 메시지 polling 및 검증 (aiokafka)
    msgs = await consumer.read_messages("file_events_base64", limit=1)
    assert msgs[0]["filename"] == "test.jpg"
    assert msgs[0]["data"]
    import base64
    decoded = base64.b64decode(msgs[0]["data"])
    assert decoded == b"testdata1234"

@pytest.mark.asyncio
async def test_api_kafka_binary(tmp_path):
    consumer = AIOKafkaConsumerImpl(brokers=BROKERS, group_id=GROUP_ID)
    producer = FastStreamKafkaProducer(brokers=BROKERS)
    await producer.broker.start()
    await asyncio.sleep(1)

    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        sample_file = tmp_path / "test.bin"
        sample_file.write_bytes(b"binarydata1234")
        with sample_file.open("rb") as f:
            files = {"file": ("test.bin", f, "application/octet-stream")}
            resp = await ac.post("/api/v1/kafka/upload-binary", files=files)
            assert resp.status_code == 200

    msgs = await consumer.read_messages("file_events_binary", limit=1)
    assert msgs[0]["filename"] == "test.bin"
    assert msgs[0]["data"]
    decoded = bytes.fromhex(msgs[0]["data"])
    assert decoded == b"binarydata1234"
