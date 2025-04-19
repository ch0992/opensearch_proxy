from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # FastAPI 테스트 클라이언트(공용)

# Item 도메인 CRUD API 테스트
# - 아이템 생성, 조회, 수정, 삭제 API를 각각 검증

def test_create_item():
    """
    아이템 생성 테스트
    새로운 아이템 정보를 POST로 보내고, 정상적으로 생성되는지 확인
    """
    resp = client.post("/api/v1/items/items/", json={"name": "item1", "description": "desc1"})
    assert resp.status_code == 200  # 생성 성공
    assert resp.json()["name"] == "item1"  # 반환값에 name 포함
    global created_item_id
    created_item_id = resp.json()["id"]

def test_get_item():
    """
    아이템 조회 테스트
    미리 생성한 아이템을 item_id로 조회해서 정보가 일치하는지 확인
    """
    resp = client.post("/api/v1/items/items/", json={"name": "item2", "description": "desc2"})  # item2 생성
    item_id = resp.json()["id"]
    resp = client.get(f"/api/v1/items/items/{item_id}")
    assert resp.status_code == 200  # 조회 성공
    assert resp.json()["name"] == "item2"  # name 일치

def test_update_item():
    """
    아이템 정보 수정 테스트
    기존 아이템의 description을 PUT으로 수정하고, 변경 사항이 반영되는지 확인
    """
    resp = client.post("/api/v1/items/items/", json={"name": "item3", "description": "desc3"})
    item_id = resp.json()["id"]
    updated = {"name": "item3", "description": "desc3-updated"}
    resp = client.put(f"/api/v1/items/items/{item_id}", json=updated)
    assert resp.status_code == 200  # 수정 성공
    assert resp.json()["description"] == "desc3-updated"  # description 변경 확인

def test_delete_item():
    """
    아이템 삭제 테스트
    아이템을 DELETE로 삭제하고, 삭제 결과 메시지가 반환되는지 확인
    """
    resp = client.post("/api/v1/items/items/", json={"name": "item4", "description": "desc4"})
    item_id = resp.json()["id"]
    resp = client.delete(f"/api/v1/items/items/{item_id}")
    assert resp.status_code == 200  # 삭제 성공
    assert "result" in resp.json()  # 삭제 결과 필드 확인
