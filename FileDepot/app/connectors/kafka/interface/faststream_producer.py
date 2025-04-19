"""
app/connectors/kafka/interface/faststream_producer.py
- FastStream 기반 Kafka 프로듀서 표준 인터페이스 및 샘플 구현
- 실제 메시지 발행 로직만 담당, 비즈니스 로직 없음
"""

from typing import Protocol, List
from faststream.kafka import KafkaBroker
from fastapi import UploadFile
import base64
import io
import zipfile

class KafkaProducer(Protocol):
    async def send(self, topic: str, message: dict): ...

from app.core.config import settings
class FastStreamKafkaProducer:
    def __init__(self, brokers: List[str] = None):
        if brokers is None:
            brokers = settings.KAFKA_BROKERS
        self.broker = KafkaBroker(",".join(brokers))
    async def send(self, topic: str, message: dict):
        await self.broker.publish(message, topic=topic)
