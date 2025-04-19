from fastapi.testclient import TestClient
from app.main import app

# 인증(로그인) API 테스트
# - 올바른 계정/비밀번호로 로그인 시 토큰이 정상 발급되는지 검증
# - 잘못된 계정/비밀번호로 로그인 시 에러가 발생하는지 검증

def test_login_success():
    """
    정상 로그인 테스트
    johndoe/secret 계정으로 로그인 요청을 보내고, access_token이 반환되는지 확인
    """
    client = TestClient(app)  # FastAPI 테스트 클라이언트 생성
    resp = client.post(
        "/api/v1/login",
        json={"username": "johndoe", "password": "secret"}  # 올바른 계정 정보
    )
    assert resp.status_code == 200  # HTTP 200 OK여야 함
    assert "access_token" in resp.json()  # access_token 필드가 반드시 존재
    assert resp.json()["token_type"] == "bearer"  # 토큰 타입이 bearer인지 확인

def test_login_fail():
    """
    실패 로그인 테스트
    존재하지 않는 계정/비밀번호로 로그인 시 401 에러와 상세 메시지 반환 확인
    """
    client = TestClient(app)
    resp = client.post(
        "/api/v1/login",
        json={"username": "wrong", "password": "wrong"}  # 잘못된 계정 정보
    )
    assert resp.status_code == 401  # 인증 실패 시 401 Unauthorized
    assert resp.json()["detail"] == "아이디 또는 비밀번호가 올바르지 않습니다."  # 에러 메시지 검증
