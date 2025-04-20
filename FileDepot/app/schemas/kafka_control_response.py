from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List

class SimpleResult(BaseModel):
    result: str = Field(..., example="ok")
    error: Optional[str] = Field(None, example="Schema validation error: ...")

class AuditLogEntry(BaseModel):
    ts: float
    topic: str
    key: Optional[str]
    payload: Dict[str, Any]
    event: str

class AuditLogList(BaseModel):
    logs: List[AuditLogEntry]

class SchemaListResponse(BaseModel):
    topics: List[str] = Field(..., example=["file_event", "user_event"])

class AllSchemasItem(BaseModel):
    topic: str = Field(..., example="file_event")
    schema_: dict = Field(..., alias="schema", example={"type": "object", "properties": {"filename": {"type": "string"}}})

class AllSchemasResponse(BaseModel):
    schemas: List[AllSchemasItem]
