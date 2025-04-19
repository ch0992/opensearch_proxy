import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.connectors.kafka.interface.aiokafka_consumer_impl import AIOKafkaConsumerImpl
from app.connectors.kafka.interface.producer import FastStreamKafkaProducer

BROKERS = ["localhost:9092"]
GROUP_ID = "test-binary-bulk"

@pytest.mark.asyncio
async def test_api_kafka_binary_bulk(tmp_path):
    consumer = AIOKafkaConsumerImpl(brokers=BROKERS, group_id=GROUP_ID)
    producer = FastStreamKafkaProducer(brokers=BROKERS)
    await producer.broker.start()
    await asyncio.sleep(1)

    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    import uuid
    filenames = []
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for i in range(10):
            unique_name = f"test_{i}_{uuid.uuid4().hex}.bin"
            filenames.append(unique_name)
            sample_file = tmp_path / unique_name
            sample_file.write_bytes(b"binarydata1234")
            with sample_file.open("rb") as f:
                files = {"file": (unique_name, f, "application/octet-stream")}
                resp = await ac.post("/api/v1/kafka/upload-binary", files=files)
                assert resp.status_code == 200

    msgs = await consumer.read_messages("file_events_binary", limit=50)  # 넉넉하게 읽어옴
    filtered_msgs = [msg for msg in msgs if msg.get("filename") in filenames]
    assert len(filtered_msgs) == 10
    for fname in filenames:
        msg = next(m for m in filtered_msgs if m["filename"] == fname)
        assert msg["data"]
        decoded = bytes.fromhex(msg["data"])
        assert decoded == b"binarydata1234"
