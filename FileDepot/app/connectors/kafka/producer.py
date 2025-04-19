"""
app/connectors/kafka/producer.py
- FastStream 기반 Kafka 프로듀서 표준 인터페이스 및 샘플 구현
- 실제 메시지 발행 로직만 담당, 비즈니스 로직 없음
"""

from faststream.kafka import KafkaProducer as FastStreamKafkaProducer

class KafkaProducer:
    def __init__(self, brokers: list[str]):
        self.producer = FastStreamKafkaProducer(brokers=brokers)

    async def send(self, topic: str, message: dict):
        """
        지정한 토픽으로 메시지를 비동기 발행
        개발자는 이 메서드만 호출하면 됨
        """
        await self.producer.send(topic, message)
