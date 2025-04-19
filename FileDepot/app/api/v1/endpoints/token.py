"""
endpoints/token.py
- 파일에 입력된 값(username, email 등)을 기반으로 JWT 토큰을 발급하는 API
- 개발/테스트 목적의 간단한 토큰 발급 예제
"""

from fastapi import APIRouter, Form
from app.core import security
from app.domain.auth.models import Token
from datetime import timedelta
from pydantic import BaseModel

from pydantic import Field

class TokenRequest(BaseModel):
    username: str = Field(..., description="사용자 계정 아이디 (예: admin)")
    password: str = Field(..., description="사용자 비밀번호 (예: admin)")

router = APIRouter()

from fastapi import HTTPException

@router.post("/generate-token", response_model=Token, tags=["example_auth"], summary="토큰 직접 발급 (입력 기반)", description="username/password를 입력받아 JWT 토큰을 발급합니다.")
def generate_token(
    username: str = Form(..., description="Swagger/관리자 계정 아이디 (예: .env에 정의된 admin)"),
    password: str = Form(..., description="Swagger/관리자 계정 비밀번호 (예: .env에 정의된 비밀번호)")
):
    """
    [관리자/Swagger 전용 토큰 발급]
    - 일반 사용자는 이 API로 인증할 수 없습니다.
    - .env에 등록된 TEST_TOKEN_USER, TEST_TOKEN_PASSWORD만 허용
    - Swagger UI 테스트 및 관리자 용도 전용

    ---
    #### 파라미터 설명
    - username: Swagger/관리자 계정 아이디 (예: .env에 정의된 admin)
    - password: Swagger/관리자 계정 비밀번호 (예: .env에 정의된 비밀번호)
    """
    from app.domain.auth.service import fake_users_db
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="관리자/Swagger 계정만 로그인 가능합니다. (.env에 등록된 계정만 허용)")
    from app.core import security
    if not security.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
    access_token = security.create_access_token(subject=username, expires_delta=timedelta(minutes=60))
    return Token(access_token=access_token, token_type="bearer")

