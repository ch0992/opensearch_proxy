"""
Oracle 커넥터 기반 CRUD Example API
- OracleConnector를 활용한 메타데이터 저장/조회 예제
- 실제 Oracle DB 연결이 필요하며, 예제는 구조와 연동 포인트에 집중
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.connectors.oracle import OracleConnector

app = FastAPI()

# Oracle 커넥터 인스턴스 (실제 환경정보로 변경 필요)
oracle = OracleConnector(dsn="mydb_high", user="admin", password="password")

# 예시 데이터 모델
class Item(BaseModel):
    id: int
    name: str
    description: str = ""

@app.post("/items/")
def create_item(item: Item):
    """Oracle에 아이템 저장 (Create)"""
    try:
        oracle.save_metadata("items", item.dict())
        return {"result": "Oracle 저장 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """(예시) Oracle에서 아이템 조회 (실제 구현 필요)"""
    # 실제 SELECT 쿼리 구현은 프로젝트에 맞게 확장 필요
    return {"result": "(예시) Oracle에서 아이템 조회"}
