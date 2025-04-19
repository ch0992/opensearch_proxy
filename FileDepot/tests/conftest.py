import pytest  # pytest: Python 테스트 프레임워크
from fastapi.testclient import TestClient  # FastAPI용 테스트 클라이언트
from app.main import app  # FastAPI 앱 인스턴스

# 모든 테스트 모듈에서 공통으로 사용할 FastAPI 테스트 클라이언트 fixture
# scope="module": 각 테스트 파일마다 한 번만 생성/공유됨
@pytest.fixture(scope="module")
def client():
    """
    FastAPI TestClient를 반환하는 pytest fixture
    - 각 테스트 함수에서 client 인자를 사용하면 이 객체가 자동 주입됨
    - 실제 서버를 띄우지 않고 HTTP 요청을 시뮬레이션 가능
    """
    return TestClient(app)
