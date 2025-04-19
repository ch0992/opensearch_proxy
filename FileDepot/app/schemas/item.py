from pydantic import BaseModel, Field
from typing import Optional

class ItemCreateRequest(BaseModel):
    name: str = Field(..., description="아이템 이름 (예: 샘플 아이템)")
    description: Optional[str] = Field('', description="아이템 설명 (예: 테스트 용도)")

class ItemUpdateRequest(BaseModel):
    name: str = Field(..., description="아이템 이름 (예: 샘플 아이템)")
    description: Optional[str] = Field('', description="아이템 설명 (예: 테스트 용도)")
