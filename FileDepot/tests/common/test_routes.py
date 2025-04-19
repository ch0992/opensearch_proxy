# FastAPI에 실제로 등록된 모든 엔드포인트 경로를 출력하는 테스트
# 이 파일을 pytest로 실행하면 등록된 route 목록을 확인할 수 있습니다.

from fastapi.testclient import TestClient
from app.main import app

def test_print_routes():
    print("\n[FastAPI 등록 엔드포인트 목록]")
    for route in app.routes:
        print(f"  {route.path}")
    # 항상 통과하도록 (실패 방지)
    assert True
