"""
service.py (domain/item)
- Item 도메인에 대한 비즈니스 로직/서비스 계층
"""

from .models import Item

# 임시 메모리 DB (실제 서비스에서는 DB로 대체)
fake_db = {}

def create_item(item: Item):
    if item.id in fake_db:
        raise ValueError("이미 존재하는 ID입니다.")
    fake_db[item.id] = item
    return item

def read_item(item_id: int):
    item = fake_db.get(item_id)
    if not item:
        raise ValueError("아이템을 찾을 수 없습니다.")
    return item

def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise ValueError("아이템을 찾을 수 없습니다.")
    fake_db[item_id] = item
    return item

def delete_item(item_id: int):
    if item_id not in fake_db:
        raise ValueError("아이템을 찾을 수 없습니다.")
    del fake_db[item_id]
    return {"result": "삭제 완료"}
