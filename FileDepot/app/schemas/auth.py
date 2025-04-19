from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="로그인할 사용자 아이디 (예: admin)")
    password: str = Field(..., description="사용자 비밀번호 (예: admin)")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT 토큰")
    token_type: str = Field(..., description="토큰 타입 (항상 'bearer')")
