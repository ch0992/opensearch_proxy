from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # FastAPI 테스트 클라이언트(공용)

# User 도메인 CRUD API 테스트
# - 사용자 생성, 조회, 수정, 삭제, 리스트 API를 각각 검증

def test_create_user():
    """
    사용자 생성 테스트
    새로운 사용자 정보를 POST로 보내고, 정상적으로 생성되는지 확인
    """
    resp = client.post("/api/v1/users/users/", json={"username": "alice", "email": "alice@example.com", "full_name": "Alice", "password": "testpw", "disabled": False})
    assert resp.status_code == 200  # 생성 성공
    assert resp.json()["username"] == "alice"  # 반환값에 username 포함
    global created_user_id
    created_user_id = resp.json()["id"]

def test_get_user():
    """
    사용자 조회 테스트
    미리 생성한 사용자를 user_id로 조회해서 정보가 일치하는지 확인
    """
    resp = client.post("/api/v1/users/users/", json={"username": "bob", "email": "bob@example.com", "full_name": "Bob", "password": "testpw", "disabled": False})  # bob 생성
    user_id = resp.json()["id"]
    resp = client.get(f"/api/v1/users/users/{user_id}")
    assert resp.status_code == 200  # 조회 성공
    assert resp.json()["username"] == "bob"  # username 일치

def test_update_user():
    """
    사용자 정보 수정 테스트
    기존 사용자의 이메일을 PUT으로 수정하고, 변경 사항이 반영되는지 확인
    """
    resp = client.post("/api/v1/users/users/", json={"username": "carol", "email": "carol@example.com", "full_name": "Carol", "password": "testpw", "disabled": False})
    user_id = resp.json()["id"]
    updated = {"username": "carol", "email": "carol@new.com", "full_name": "Carol", "password": "testpw", "disabled": False}
    resp = client.put(f"/api/v1/users/users/{user_id}", json=updated)
    assert resp.status_code == 200  # 수정 성공
    assert resp.json()["email"] == "carol@new.com"  # 이메일 변경 확인

def test_delete_user():
    """
    사용자 삭제 테스트
    사용자를 DELETE로 삭제하고, 삭제 결과 메시지가 반환되는지 확인
    """
    resp = client.post("/api/v1/users/users/", json={"username": "dave", "email": "dave@example.com", "full_name": "Dave", "password": "testpw", "disabled": False})
    user_id = resp.json()["id"]
    resp = client.delete(f"/api/v1/users/users/{user_id}")
    assert resp.status_code == 200  # 삭제 성공
    assert "result" in resp.json()  # 삭제 결과 필드 확인

def test_list_users():
    """
    사용자 리스트 조회 테스트
    전체 사용자 목록을 GET으로 받아 리스트 타입인지 확인
    """
    resp = client.get("/api/v1/users/users/")
    assert resp.status_code == 200  # 조회 성공
    assert isinstance(resp.json(), list)  # 반환값이 리스트인지 확인
