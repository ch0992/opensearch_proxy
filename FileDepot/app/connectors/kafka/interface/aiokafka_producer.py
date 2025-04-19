"""
app/connectors/kafka/interface/aiokafka_producer.py
- aiokafka 기반 Kafka 프로듀서 표준 인터페이스 및 샘플 구현
- 실제 메시지 발행 로직만 담당, 비즈니스 로직 없음
"""

from typing import Optional, List
from aiokafka import AIOKafkaProducer
import asyncio
from app.core.config import settings

class AIOKafkaProducerWrapper:
    def __init__(self, brokers: Optional[List[str]] = None):
        if brokers is None:
            brokers = settings.KAFKA_BROKERS
        self.brokers = brokers
        self._producer = None

    async def start(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
            await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send(self, topic: str, value: bytes, key: bytes = None):
        await self.start()
        await self._producer.send_and_wait(topic, value=value, key=key)

    async def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1):
        # 토픽 생성은 일반적으로 admin client로 처리해야 함
        from aiokafka.admin import AIOKafkaAdminClient, NewTopic
        admin_client = AIOKafkaAdminClient(bootstrap_servers=self.brokers)
        await admin_client.start()
        try:
            topic_obj = NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)
            await admin_client.create_topics([topic_obj])
        finally:
            await admin_client.close()
