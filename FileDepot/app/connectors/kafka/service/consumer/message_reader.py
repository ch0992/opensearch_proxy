from app.connectors.kafka.interface.aiokafka_consumer import AIOKafkaConsumer
from typing import Optional, List

class MessageReader:
    def __init__(self, consumer: AIOKafkaConsumer):
        self.consumer = consumer

    async def list_topics(self) -> list[str]:
        # Dummy implementation for testing/patching
        raise NotImplementedError

    async def read_messages(self, topic: str, limit: int = 10, partition: Optional[int] = None, offset: Optional[int] = None, key: Optional[str] = None) -> List[dict]:
        return await self.consumer.read_messages(topic, limit, partition, offset, key)
