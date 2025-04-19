"""
models.py (domain/item)
- Item 도메인에 대한 데이터/비즈니스 모델 정의
"""

from pydantic import BaseModel

from pydantic import Field

class Item(BaseModel):
    id: int = Field(..., description="아이템 고유 ID (예: 1)", example=1)
    name: str = Field(..., description="아이템 이름 (예: 샘플 아이템)", example="샘플 아이템")
    description: str = Field("", description="아이템 설명 (예: 테스트 용도)", example="테스트 용도")
