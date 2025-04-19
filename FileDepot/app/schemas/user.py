from pydantic import BaseModel, Field
from typing import Optional

class UserCreateRequest(BaseModel):
    username: str = Field(..., description="사용자 계정 아이디 (예: admin)")
    email: str = Field(..., description="사용자 이메일 (예: test@example.com)")
    full_name: str = Field(..., description="사용자 이름 (예: 홍길동)")
    password: str = Field(..., description="사용자 비밀번호 (예: admin)")
    disabled: Optional[bool] = Field(False, description="비활성화 여부 (예: false)")

class UserUpdateRequest(BaseModel):
    username: str = Field(..., description="사용자 계정 아이디 (예: admin)")
    email: str = Field(..., description="사용자 이메일 (예: test@example.com)")
    full_name: str = Field(..., description="사용자 이름 (예: 홍길동)")
    password: str = Field(..., description="사용자 비밀번호 (예: admin)")
    disabled: Optional[bool] = Field(False, description="비활성화 여부 (예: false)")
