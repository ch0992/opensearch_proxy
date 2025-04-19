import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from app.main import app

@pytest.mark.asyncio
@patch("app.connectors.kafka.service.consumer.message_reader.MessageReader.list_topics", new_callable=AsyncMock)
async def test_kafka_list_topics(mock_list_topics):
    mock_list_topics.return_value = ["topic1", "topic2"]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/v1/kafka/topics")
        assert resp.status_code == 200
        assert set(resp.json()["topics"]) == {"file_events_base64", "file_events_binary"}

@pytest.mark.asyncio
@patch("app.connectors.kafka.service.consumer.message_reader.MessageReader.read_messages", new_callable=AsyncMock)
async def test_kafka_messages_limit(mock_read_messages):
    mock_read_messages.return_value = [
        {"offset": 1, "partition": 0, "key": None, "value": "msg1", "timestamp": 1234567890},
        {"offset": 2, "partition": 0, "key": None, "value": "msg2", "timestamp": 1234567891}
    ]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/v1/kafka/messages?topic=test-topic&limit=2")
        assert resp.status_code == 200
        assert len(resp.json()["messages"]) == 2

@pytest.mark.asyncio
@patch("app.connectors.kafka.service.consumer.message_reader.MessageReader.read_messages", new_callable=AsyncMock)
async def test_kafka_messages_key_filter(mock_read_messages):
    mock_read_messages.return_value = [
        {"offset": 3, "partition": 0, "key": "mykey", "value": "msg-key", "timestamp": 1234567892}
    ]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/v1/kafka/messages?topic=test-topic&key=mykey")
        assert resp.status_code == 200
        assert resp.json()["messages"][0]["key"] == "mykey"

@pytest.mark.asyncio
@patch("app.connectors.kafka.service.consumer.message_reader.MessageReader.read_messages", new_callable=AsyncMock)
async def test_kafka_messages_partition_offset(mock_read_messages):
    mock_read_messages.return_value = [
        {"offset": 10, "partition": 1, "key": None, "value": "msg10", "timestamp": 1234567893}
    ]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/v1/kafka/messages?topic=test-topic&partition=1&offset=10&limit=1")
        assert resp.status_code == 200
        assert resp.json()["messages"][0]["offset"] == 10
        assert resp.json()["messages"][0]["partition"] == 1
