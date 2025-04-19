"""
endpoints/auth.py
- 인증/인가 관련 FastAPI 엔드포인트 (로그인 등)
"""

from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, TokenResponse
from app.domain.auth.service import authenticate_user, create_access_token_for_user

router = APIRouter()



@router.post(
    "/login",
    response_model=TokenResponse,
    tags=["example_auth"],
    summary="로그인 (사용자 인증 및 토큰 발급)",
    description="사용자 로그인을 수행하고, 인증 토큰(JWT)을 발급하는 예제 API입니다.\n\n- username: 로그인할 사용자 아이디 (예: admin)\n- password: 사용자 비밀번호 (예: admin)"
)
def login(request: LoginRequest):
    """
    사용자 인증(로그인) 및 토큰 발급 예제. Request body로 username, password를 입력받습니다.
    ---
    #### 파라미터 설명
    - username: 로그인할 사용자 아이디 (예: admin)
    - password: 사용자 비밀번호 (예: admin)
    """
    print(f"[로그인 요청] username={request.username}, password=***")
    user = authenticate_user(request.username, request.password)
    if not user:
        print(f"[로그인 실패] username={request.username}, 비밀번호 불일치 또는 사용자 없음")
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")
    print(f"[로그인 성공] {user}")
    token = create_access_token_for_user(user)
    return TokenResponse(access_token=token.access_token, token_type=token.token_type)
