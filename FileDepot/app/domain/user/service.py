"""
service.py (domain/user)
- User 도메인 비즈니스 로직 (CRUD)
"""

from .models import User
from typing import List, Optional

# 임시 메모리 DB (실제 서비스에서는 DB 연동 필요)
fake_users_db = {}

def create_user(user: User) -> User:
    if user.id in fake_users_db:
        raise ValueError("이미 존재하는 ID입니다.")
    fake_users_db[user.id] = user
    return user

def get_user(user_id: int) -> Optional[User]:
    return fake_users_db.get(user_id)

def update_user(user_id: int, user: User) -> User:
    if user_id not in fake_users_db:
        raise ValueError("사용자를 찾을 수 없습니다.")
    fake_users_db[user_id] = user
    return user

def delete_user(user_id: int) -> dict:
    if user_id not in fake_users_db:
        raise ValueError("사용자를 찾을 수 없습니다.")
    del fake_users_db[user_id]
    return {"result": "삭제 완료"}

def list_users() -> List[User]:
    return list(fake_users_db.values())
