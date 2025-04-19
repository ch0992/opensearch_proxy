"""
endpoints/users.py
- User 도메인 CRUD FastAPI 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Path, Form
from typing import List
from app.schemas.user import UserCreateRequest, UserUpdateRequest
from app.domain.user.models import User
from app.domain.user.service import create_user, get_user, update_user, delete_user, list_users

router = APIRouter()

@router.post(
    "/users/",
    response_model=User,
    tags=["example_users"],
    summary="사용자 생성",
    description="새로운 사용자 등록 예제 API"
)
def create(
    username: str = Form(..., description="사용자 계정 아이디 (예: admin)"),
    email: str = Form(..., description="사용자 이메일 (예: test@example.com)"),
    full_name: str = Form(..., description="사용자 이름 (예: 홍길동)"),
    password: str = Form(..., description="사용자 비밀번호 (예: admin)"),
    disabled: bool = Form(False, description="비활성화 여부 (예: false)")
):
    """
    새로운 사용자 등록 예제 API
    ---
    #### 파라미터 설명
    - username: 사용자 계정 아이디 (예: admin)
    - email: 사용자 이메일 (예: test@example.com)
    - full_name: 사용자 이름 (예: 홍길동)
    - password: 사용자 비밀번호 (예: admin)
    - disabled: 비활성화 여부 (예: false)
    """
    import uuid
    user_id = uuid.uuid4().int >> 96  # 32비트 int
    user = User(
        id=user_id,
        username=request.username,
        email=request.email,
        full_name=request.full_name,
        disabled=request.disabled
    )
    print(f"[사용자 생성 요청] 입력값: username={request.username}, email={request.email}, full_name={request.full_name}, disabled={request.disabled}")
    print(f"[사용자 생성 결과] User 객체: {user}")
    try:
        return create_user(user)
    except ValueError as e:
        print(f"[사용자 생성 오류] {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/users/{user_id}",
    response_model=User,
    tags=["example_users"],
    summary="사용자 조회 (Read)",
    description="특정 사용자 정보 읽기 예제 API"
)
def read(user_id: int):
    print(f"[사용자 조회 요청] user_id={user_id}")
    user = get_user(user_id)
    if not user:
        print(f"[사용자 조회 오류] user_id={user_id} 사용자를 찾을 수 없습니다.")
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    print(f"[사용자 조회 결과] {user}")
    return user

@router.put(
    "/users/{user_id}",
    response_model=User,
    tags=["example_users"],
    summary="사용자 수정",
    description="사용자 정보 수정 예제 API"
)
def update(
    user_id: int = Path(..., description="수정할 사용자 고유 ID (예: 1)"),
    username: str = Form(..., description="사용자 계정 아이디 (예: admin)"),
    email: str = Form(..., description="사용자 이메일 (예: test@example.com)"),
    full_name: str = Form(..., description="사용자 이름 (예: 홍길동)"),
    password: str = Form(..., description="사용자 비밀번호 (예: admin)"),
    disabled: bool = Form(False, description="비활성화 여부 (예: false)")
):
    """
    사용자 정보 수정 예제 API
    ---
    #### 파라미터 설명
    - user_id: 수정할 사용자 고유 ID (예: 1)
    - username: 사용자 계정 아이디 (예: admin)
    - email: 사용자 이메일 (예: test@example.com)
    - full_name: 사용자 이름 (예: 홍길동)
    - password: 사용자 비밀번호 (예: admin)
    - disabled: 비활성화 여부 (예: false)
    """
    print(f"[사용자 수정 요청] user_id={user_id}, username={request.username}, email={request.email}, full_name={request.full_name}, disabled={request.disabled}")
    try:
        user = User(
            id=user_id,
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            disabled=request.disabled
        )
        return update_user(user_id, user)
    except ValueError as e:
        print(f"[사용자 수정 오류] user_id={user_id}, {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete(
    "/users/{user_id}",
    tags=["example_users"],
    summary="사용자 삭제",
    description="사용자 정보 삭제 예제 API"
)
def delete(
    user_id: int = Path(..., description="삭제할 사용자 고유 ID (예: 1)")
):
    """
    사용자 정보 삭제 예제 API

    ---
    #### 파라미터 설명
    - user_id: 삭제할 사용자 고유 ID (예: 1)
    """
    print(f"[사용자 삭제 요청] user_id={user_id}")
    try:
        result = delete_user(user_id)
        print(f"[사용자 삭제 결과] {result}")
        return result
    except ValueError as e:
        print(f"[사용자 삭제 오류] user_id={user_id}, {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/users/",
    response_model=List[User],
    tags=["example_users"],
    summary="사용자 전체 목록 조회 (Read)",
    description="전체 사용자 목록을 읽는 예제 API"
)
def list_all():
    users = list_users()
    print(f"[사용자 전체 목록 조회] 총 {len(users)}명 사용자 반환")
    return users
