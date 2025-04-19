"""
Kafka 커넥터(FastStream) 기반 CRUD Example API
- KafkaProducer/KafkaConsumer를 활용한 메시지 기반 CRUD 예제
- 실제 DB 없이 메시지 발행/수신 구조만 구현
- FastAPI와 커넥터 연동 포인트를 명확히 주석 처리
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from app.connectors.kafka.producer import KafkaProducer
from app.connectors.kafka.consumer import KafkaConsumer
import asyncio

app = FastAPI()

# Kafka 커넥터 인스턴스 생성 (실제 브로커 주소로 변경 필요)
import os
kafka_producer = KafkaProducer(brokers=os.getenv("KAFKA_BROKERS", "localhost:9092").split(","))
kafka_consumer = KafkaConsumer(brokers=os.getenv("KAFKA_BROKERS", "localhost:9092").split(","), group_id=os.getenv("KAFKA_GROUP_ID", "crud-group"))

# 예시 데이터 모델
class Item(BaseModel):
    id: int
    name: str
    description: str = ""

# 메시지 발행 (Create/Update/Delete)
@app.post("/items/")
async def create_item(item: Item):
    await kafka_producer.send("crud-create", item.dict())
    return {"result": "메시지 발행 완료 (Create)"}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    await kafka_producer.send("crud-update", item.dict())
    return {"result": "메시지 발행 완료 (Update)"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    await kafka_producer.send("crud-delete", {"id": item_id})
    return {"result": "메시지 발행 완료 (Delete)"}

# 메시지 수신 예시 (Read)
received_items: Dict[int, Item] = {}

async def handle_create(message):
    item = Item(**message)
    received_items[item.id] = item

async def handle_update(message):
    item = Item(**message)
    received_items[item.id] = item

async def handle_delete(message):
    item_id = message["id"]
    received_items.pop(item_id, None)

# Kafka 토픽 구독 및 핸들러 등록
def start_kafka_consumers():
    kafka_consumer.subscribe("crud-create", handle_create)
    kafka_consumer.subscribe("crud-update", handle_update)
    kafka_consumer.subscribe("crud-delete", handle_delete)

# FastAPI 서버 시작 시 Kafka 컨슈머 등록 (비동기 백그라운드)
@app.on_event("startup")
def on_startup():
    start_kafka_consumers()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = received_items.get(item_id)
    if not item:
        return {"error": "아이템을 찾을 수 없습니다."}
    return item
