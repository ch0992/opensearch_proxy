"""
app/connectors/kafka/interface/faststream_consumer.py
- FastStream 기반 Kafka 컨슈머 표준 인터페이스 및 샘플 구현
- 실제 메시지 수신/콜백 등록만 담당, 비즈니스 로직 없음
"""

from typing import Protocol, Optional, List

from typing import Protocol, Callable, Any, List
from faststream.kafka import KafkaBroker

class KafkaConsumer(Protocol):
    async def subscribe(self, topic: str, handler: Callable[[dict], Any]): ...

class FastStreamKafkaConsumer(KafkaConsumer):
    def __init__(self, brokers: List[str]):
        self.broker = KafkaBroker(",".join(brokers))

    async def subscribe(self, topic: str, handler: Callable[[dict], Any]):
        @self.broker.subscriber(topic)
        async def _handler(msg):
            await handler(msg)
        await self.broker.start()

# (이전 aiokafka 기반 구현체는 제거 또는 별도 파일로 분리)
