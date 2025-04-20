"""
Kafka Control Plane API Logic (FastAPI + FastStream 기반)
- 메시지 스키마 관리 (메모리)
- 메시지 발행/검증/조회/재전송 등 핵심 비즈니스 로직
"""
from typing import Any, Dict, List, Optional
from faststream.kafka import KafkaBroker
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException
import jsonschema
import time
import threading

# --- In-memory schema & audit log storage ---
SCHEMA_REGISTRY: Dict[str, dict] = {}
AUDIT_LOG: List[dict] = []

# Kafka 브로커 인스턴스 (FastStream)
from app.core.config import settings

# settings.KAFKA_BROKERS는 문자열 또는 리스트일 수 있음
brokers = getattr(settings, "KAFKA_BROKERS", None)
if not brokers:
    brokers = ["localhost:9092"]
if isinstance(brokers, str):
    brokers = [b.strip() for b in brokers.split(",") if b.strip()]
broker = KafkaBroker(",".join(brokers))

# --- 메시지 발행 ---
async def publish_message(topic: str, key: Optional[str], payload: dict) -> dict:
    schema = SCHEMA_REGISTRY.get(topic)
    if schema:
        try:
            jsonschema.validate(instance=payload, schema=schema)
        except jsonschema.ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Schema validation error: {e}")
    # 브로커 연결 (이미 연결되어 있으면 내부적으로 무시됨)
    await broker.start()
    # 발행 (비동기)
    # Kafka key는 bytes 또는 None이어야 함
    key_bytes = key.encode("utf-8") if isinstance(key, str) else key
    await broker.publish(payload, topic=topic, key=key_bytes)
    # 감사 로그 기록
    AUDIT_LOG.append({
        "ts": time.time(),
        "topic": topic,
        "key": key,
        "payload": payload,
        "event": "publish"
    })
    return {"result": "ok"}

# --- 메시지 dry-run (스키마 검증만) ---
def dry_run(topic: str, payload: dict) -> dict:
    schema = SCHEMA_REGISTRY.get(topic)
    if not schema:
        return {
            "result": "not_found",
            "message": "등록된 스키마가 없습니다.",
            "error": None
        }
    try:
        jsonschema.validate(instance=payload, schema=schema)
        return {
            "result": "valid",
            "message": "메시지 포맷이 스키마에 적합합니다.",
            "error": None
        }
    except jsonschema.ValidationError as e:
        return {
            "result": "invalid",
            "message": "메시지 포맷이 스키마에 맞지 않습니다.",
            "error": str(e)
        }

# --- 스키마 등록/조회 ---
def register_schema(topic: str, schema: dict, sample_payload: dict = None) -> dict:
    # 1. 스키마 문법 검증
    try:
        jsonschema.Draft7Validator.check_schema(schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Schema syntax error: {e}")
    # 2. dry-run: 샘플 payload가 있으면 검증
    if sample_payload is not None:
        try:
            jsonschema.validate(instance=sample_payload, schema=schema)
        except jsonschema.ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Sample payload dry-run failed: {e}")
    SCHEMA_REGISTRY[topic] = schema
    return {"result": "registered"}

def get_schema(topic: str) -> dict:
    schema = SCHEMA_REGISTRY.get(topic)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema

def list_schemas() -> List[str]:
    return list(SCHEMA_REGISTRY.keys())

def get_all_schemas() -> list:
    """전체 토픽-스키마 쌍을 리스트로 반환"""
    # 빈 스키마도 빈 리스트로 반환 (예외 X)
    return [
        {"topic": topic, "schema_": schema}
        for topic, schema in SCHEMA_REGISTRY.items()
    ]

# --- 감사 로그 조회 ---
def get_audit_log(limit: int = 100) -> List[dict]:
    return AUDIT_LOG[-limit:][::-1]
