"""
service.py (domain/auth)
- 인증/인가 관련 서비스 로직 (JWT 발급, 패스워드 검증 등)
"""

from datetime import timedelta
from typing import Optional
from app.core import security
from .models import UserInDB, User, Token

# 예시 유저 DB (실제 서비스에서는 DB 연동 필요)
from app.core.config import settings

fake_users_db = {
    "johndoe": UserInDB(username="johndoe", email="johndoe@example.com", full_name="John Doe", hashed_password=security.get_password_hash("secret"), disabled=False),
    "test": UserInDB(username="test", email="test@example.com", full_name="테스트유저", hashed_password=security.get_password_hash("1"), disabled=False)
}

# .env에 TEST_TOKEN_USER, TEST_TOKEN_PASSWORD가 있으면 admin 계정 자동 등록
admin_user = getattr(settings, "TEST_TOKEN_USER", None)
admin_pw = getattr(settings, "TEST_TOKEN_PASSWORD", None)
if admin_user and admin_pw:
    fake_users_db[admin_user] = UserInDB(
        username=admin_user,
        email=f"{admin_user}@example.com",
        full_name="관리자",
        hashed_password=security.get_password_hash(admin_pw),
        disabled=False
    )


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = fake_users_db.get(username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token_for_user(user: UserInDB) -> Token:
    access_token = security.create_access_token(subject=user.username, expires_delta=timedelta(minutes=30))
    return Token(access_token=access_token, token_type="bearer")
