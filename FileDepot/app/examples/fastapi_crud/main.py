"""
FastAPI 기반 CRUD Example API
- 메모리 내 데이터 저장소를 활용한 간단한 CRUD 예제
- FastAPI 기본 기능만 사용
- 초보자도 따라할 수 있도록 구조와 주석을 명확히 작성
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 데이터 저장을 위한 임시 메모리 DB
fake_db = {}

# Pydantic 모델 정의
class Item(BaseModel):
    id: int
    name: str
    description: str = ""

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    """아이템 생성 (Create)"""
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")
    fake_db[item.id] = item
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    """아이템 조회 (Read)"""
    item = fake_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    """아이템 수정 (Update)"""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    fake_db[item_id] = item
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """아이템 삭제 (Delete)"""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    del fake_db[item_id]
    return {"result": "삭제 완료"}
