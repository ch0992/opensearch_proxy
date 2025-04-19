from typing import Optional, List

class AIOKafkaConsumer:
    def __init__(self, brokers: Optional[list[str]] = None, group_id: Optional[str] = None):
        import os
        if brokers is None:
            brokers = os.getenv("KAFKA_BROKERS", "localhost:9092").split(",")
        self.brokers = brokers
        self.group_id = group_id

    async def read_messages(self, topic: str, limit: int = 10, partition: Optional[int] = None, offset: Optional[int] = None, key: Optional[str] = None) -> List[dict]:
        """
        Kafka 토픽에서 메시지를 조회합니다. 최대 limit만큼 메시지를 가져오며,
        메시지가 없으면 최대 2초까지만 대기 후, 수집된 메시지를 반환합니다.
        """
        from aiokafka import AIOKafkaConsumer
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.brokers,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id=self.group_id,
        )
        await consumer.start()
        try:
            if partition is not None:
                partitions = [p for p in await consumer.partitions_for_topic(topic) if p == partition]
                if not partitions:
                    return []
                tp = consumer._create_tp(topic, partition)
                await consumer.assign([tp])
                if offset is not None:
                    await consumer.seek(tp, offset)
            import asyncio
            msgs = []
            try:
                async with asyncio.timeout(2):  # 2초 타임아웃
                    async for msg in consumer:
                        msg_key = msg.key.decode() if msg.key else None
                        if key and msg_key != key:
                            continue
                        import json
                        value_str = msg.value.decode(errors="replace")
                        try:
                            value = json.loads(value_str)
                        except Exception:
                            value = value_str
                        msg_dict = {
                            "offset": msg.offset,
                            "partition": msg.partition,
                            "key": msg_key,
                            "timestamp": msg.timestamp
                        }
                        if isinstance(value, dict):
                            msg_dict.update(value)
                        else:
                            msg_dict["value"] = value
                        msgs.append(msg_dict)
                        if len(msgs) >= limit:
                            break
            except (asyncio.TimeoutError, TimeoutError):
                pass
            return msgs
        finally:
            await consumer.stop()
