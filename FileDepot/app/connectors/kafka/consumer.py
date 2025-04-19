"""
app/connectors/kafka/consumer.py
- FastStream 기반 Kafka 컨슈머 표준 인터페이스 및 샘플 구현
- 실제 메시지 수신/콜백 등록만 담당, 비즈니스 로직 없음
"""

from faststream.kafka import KafkaBroker

class KafkaConsumer:
    def __init__(self, brokers: list[str], group_id: str):
        self.broker = KafkaBroker(brokers=brokers, group_id=group_id)

    def subscribe(self, topic: str, handler):
        """
        토픽 구독 및 메시지 핸들러 등록
        handler: async def handler(message) 형태의 콜백
        """
        @self.broker.subscriber(topic)
        async def on_message(message):
            await handler(message)
