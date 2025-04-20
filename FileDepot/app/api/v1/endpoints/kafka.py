"""
endpoints/kafka.py
- Kafka 연동 테스트용 FastAPI 엔드포인트 (base64, 바이너리 업로드 분리)
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional

from app.connectors.kafka.interface.faststream_producer import FastStreamKafkaProducer
from app.connectors.kafka.interface.faststream_consumer import FastStreamKafkaConsumer
from app.connectors.kafka.interface.aiokafka_consumer import AIOKafkaConsumer
from app.connectors.kafka.interface.aiokafka_producer import AIOKafkaProducerWrapper
from app.connectors.kafka.service.producer.file_uploader import FileUploader
from app.connectors.kafka.service.consumer.message_reader import MessageReader


router = APIRouter()
from app.core.config import settings

def parse_brokers(val):
    if isinstance(val, str):
        return [b.strip() for b in val.split(",") if b.strip()]
    return list(val)

brokers = parse_brokers(getattr(settings, "KAFKA_BROKERS", "localhost:9092"))

faststream_producer = FastStreamKafkaProducer(brokers=brokers)
aiokafka_producer = AIOKafkaProducerWrapper(brokers=brokers)
faststream_consumer = FastStreamKafkaConsumer(brokers=brokers)
aiokafka_consumer = AIOKafkaConsumer(brokers=brokers)
file_uploader = FileUploader(faststream_producer)
message_reader = MessageReader(aiokafka_consumer)

@router.post(
    "/kafka/faststream/upload-base64",
    tags=["faststream"],
    summary="[Faststream Producer] Base64 파일 업로드 (Kafka 메시지 발행)",
    description="[Faststream] 단일 파일 또는 ZIP 파일을 업로드하면, 파일 내용을 base64로 인코딩하여 Kafka로 발행합니다. ZIP 파일의 경우 내부 모든 파일을 개별 메시지로 발행합니다."
)
async def upload_faststream_base64(file: UploadFile = File(...)):
    await file_uploader.send_file_base64("file_events_base64", file)
    return {"result": "queued (faststream base64)"}

@router.post(
    "/kafka/faststream/upload-binary",
    tags=["faststream"],
    summary="[Faststream Producer] 바이너리 파일 업로드 (Kafka 메시지 발행)",
    description="[Faststream] 단일 파일 또는 ZIP 파일을 업로드하면, 파일 내용을 바이너리(hex)로 Kafka에 발행합니다. ZIP 파일의 경우 내부 모든 파일을 개별 메시지로 발행합니다."
)
async def upload_faststream_binary(file: UploadFile = File(...)):
    await file_uploader.send_file_binary("file_events_binary", file)
    return {"result": "queued (faststream binary)"}


@router.post(
    "/kafka/aiokafka/create-topic",
    tags=["aiokafka"],
    summary="[aiokafka Admin] Kafka 토픽 생성",
    description="[aiokafka] Kafka 토픽을 생성합니다. (admin client 사용)"
)
async def create_aiokafka_topic(
    topic: str,
    num_partitions: int = 1,
    replication_factor: int = 1
):
    await aiokafka_producer.create_topic(topic, num_partitions, replication_factor)
    return {"result": f"topic '{topic}' created"}

@router.get(
    "/kafka/aiokafka/topics",
    tags=["aiokafka"],
    summary="[aiokafka Admin] Kafka 토픽 전체 목록 조회",
    description="[aiokafka] Kafka 브로커에 존재하는 모든 토픽 리스트를 반환합니다. (실제 admin client 사용)"
)
async def aiokafka_list_topics():
    from aiokafka.admin import AIOKafkaAdminClient
    admin_client = AIOKafkaAdminClient(bootstrap_servers=aiokafka_producer.brokers)
    await admin_client.start()
    try:
        topics = await admin_client.list_topics()
    finally:
        await admin_client.close()
    return {"topics": list(topics)}

@router.get(
    "/kafka/aiokafka/messages",
    tags=["aiokafka"],
    summary="[aiokafka Consumer] Kafka 메시지 조회",
    description="[aiokafka] Kafka 토픽에서 메시지를 조회합니다. (테스트/개발용, aiokafka consumer 직접 사용)"
)
async def get_kafka_messages_aiokafka(
    topic: str = Query(..., description="조회할 Kafka 토픽명"),
    limit: int = Query(10, description="조회할 메시지 개수 (기본 10)"),
    partition: Optional[int] = Query(None, description="파티션 번호 (옵션)"),
    offset: Optional[int] = Query(None, description="offset 지정 (옵션)"),
    key: Optional[str] = Query(None, description="메시지 key 필터 (옵션)")
):
    msgs = await message_reader.read_messages(topic, limit, partition, offset, key)
    return {"messages": msgs}
