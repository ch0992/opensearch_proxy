"""
models.py (domain/user)
- User 도메인 모델 정의 (DB/Pydantic)
"""

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
