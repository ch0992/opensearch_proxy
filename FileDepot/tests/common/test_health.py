from fastapi.testclient import TestClient
from app.main import app

# 루트(헬스체크) 엔드포인트 테스트
# - 서버가 정상적으로 동작하는지, 기본 응답이 올바른지 검증

def test_root():
    """
    루트(/) 엔드포인트 헬스체크 테스트
    서버가 정상적으로 기동되어 있고, 기본 메시지가 포함되어 있는지 확인
    """
    client = TestClient(app)  # FastAPI 테스트 클라이언트 생성
    resp = client.get("/")  # 루트 엔드포인트 GET 요청
    assert resp.status_code == 200  # HTTP 200 OK여야 함
    assert "message" in resp.json()  # 응답에 'message' 필드가 포함되어야 함
