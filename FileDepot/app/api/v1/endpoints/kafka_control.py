"""
Kafka Control Plane API (FastAPI + FastStream)
- 메시지 발행/스키마 관리/검증/조회/재전송 등
"""
from fastapi import APIRouter, HTTPException
from app.domain.kafka import control_plane
from app.schemas.kafka_control import PublishRequest, RegisterSchemaRequest, DryRunRequest
from app.schemas.kafka_control_response import SimpleResult, AuditLogList, SchemaListResponse, AllSchemasResponse

router = APIRouter()

# 1. 메시지 발행 API
@router.post("/publish", tags=["kafka"], response_model=SimpleResult)
async def publish(req: PublishRequest):
    """Kafka 메시지 발행 (스키마 검증 포함)"""
    return await control_plane.publish_message(req.topic, req.key, req.payload)

# 2. 메시지 스키마 등록
@router.post("/schema/register", tags=["kafka"], response_model=SimpleResult)
def register_schema(req: RegisterSchemaRequest):
    """
    Kafka 메시지 스키마 등록 (문법 검증 및 dry-run 통과 시에만 등록)
    - sample_payload를 함께 보내면 해당 스키마로 dry-run 검증까지 수행
    """
    return control_plane.register_schema(req.topic, req.message_schema, req.sample_payload)

# 2-2. 메시지 스키마 조회
@router.get("/schema/{topic}", tags=["kafka"])
def get_schema(topic: str):
    """Kafka 메시지 스키마 조회"""
    return control_plane.get_schema(topic)

# 2-3. 메시지 스키마 리스트 조회
@router.get("/schema", tags=["kafka"], response_model=SchemaListResponse)
def list_schemas():
    """등록된 메시지 스키마(토픽) 리스트 조회"""
    return {"topics": control_plane.list_schemas()}

# 2-4. 전체 메시지 스키마 일괄 조회
@router.get("/schema/all", tags=["kafka"], response_model=AllSchemasResponse)
def get_all_schemas():
    """전체 토픽-메시지스키마 쌍을 일괄 조회"""
    schemas = control_plane.get_all_schemas()
    return AllSchemasResponse(schemas=schemas)

# 3. 메시지 유효성 사전 검사 API
@router.post("/dry-run", tags=["kafka"], response_model=SimpleResult)
def dry_run(req: DryRunRequest):
    """Kafka 메시지 포맷 검증 (dry-run)"""
    return control_plane.dry_run(req.topic, req.payload)

# 4. 감사 로그 API
@router.get("/audit-log", tags=["kafka"], response_model=AuditLogList)
def audit_log(limit: int = 100):
    """메시지 발행 이력 조회"""
    return {"logs": control_plane.get_audit_log(limit)}
