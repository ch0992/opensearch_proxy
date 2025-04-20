from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class PublishRequest(BaseModel):
    topic: str = Field(..., example="file_event", description="Kafka 토픽명")
    key: Optional[str] = Field(None, example="file-001", description="Kafka 메시지 키")
    payload: Dict[str, Any] = Field(..., example={
        "filename": "test.txt",
        "content_type": "text/plain",
        "data": "SGVsbG8gd29ybGQ=",
        "meta": {"user": "admin"}
    }, description="Kafka 메시지 본문")

class RegisterSchemaRequest(BaseModel):
    topic: str = Field(..., example="file_event", description="Kafka 토픽명")
    message_schema: dict = Field(
        ...,
        alias="schema",
        example={
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content_type": {"type": "string"},
                "data": {"type": "string"},
                "meta": {"type": "object"}
            },
            "required": ["filename", "content_type", "data"]
        },
        description="Kafka 메시지 JSON Schema"
    )
    sample_payload: Optional[dict] = Field(None, example={
        "filename": "test.txt",
        "content_type": "text/plain",
        "data": "SGVsbG8gd29ybGQ=",
        "meta": {"user": "admin"}
    }, description="스키마 검증용 샘플 메시지")

    class Config:
        allow_population_by_field_name = True

class DryRunRequest(BaseModel):
    topic: str = Field(..., example="file_event")
    payload: Dict[str, Any] = Field(..., example={
        "filename": "test.txt",
        "content_type": "text/plain",
        "data": "SGVsbG8gd29ybGQ=",
        "meta": {"user": "admin"}
    })
