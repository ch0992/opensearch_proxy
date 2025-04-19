"""
app/examples/fastapi_example.py
- 커넥터 표준을 활용한 FastAPI 연동 예시
- 실제 서비스 개발자가 참고할 샘플
"""

from fastapi import FastAPI
from app.connectors.kafka.producer import KafkaProducer
from app.connectors.minio import MinioConnector

app = FastAPI()

# 커넥터 인스턴스 생성 예시
from app.core.config import settings
kafka_producer = KafkaProducer(brokers=settings.KAFKA_BROKERS)
minio_client = MinioConnector(endpoint=settings.MINIO_ENDPOINT, access_key=settings.MINIO_ACCESS_KEY, secret_key=settings.MINIO_SECRET_KEY)

@app.post("/send-event")
async def send_event(data: dict):
    # Kafka로 메시지 발행
    await kafka_producer.send("events", data)
    return {"result": "sent"}

@app.post("/upload-file")
def upload_file():
    # MinIO 파일 업로드 예시
    minio_client.upload_file("mybucket", "/tmp/test.txt", "test.txt")
    return {"result": "uploaded"}
