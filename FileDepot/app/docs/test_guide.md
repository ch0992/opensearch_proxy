# FileDepot 테스트 가이드

FileDepot 프로젝트의 테스트 구조, 실행 방법, 주요 테스트 케이스, 그리고 **새로운 테스트 코드를 작성할 때 따라야 할 가이드**를 제공합니다.

---

## 예시 테스트 구조

```
FileDepot/
  tests/
    auth/         # 인증 API 테스트
      test_auth.py
    user/         # 사용자 CRUD API 테스트
      test_user_crud.py
    item/         # 아이템 CRUD API 테스트
      test_item_crud.py
    common/       # 공통(헬스체크, 라우트 등) 테스트
      test_health.py
      test_routes.py
    conftest.py   # 공통 fixture 정의
```

---

## 테스트 작성 가이드 (개발자용)

FileDepot의 테스트 코드는 다음 원칙을 따릅니다.

1. **테스트 함수명은 반드시 `test_`로 시작**
2. **테스트 목적, 입력, 기대 결과를 docstring과 주석으로 상세하게 작성**
3. **FastAPI TestClient를 활용해 실제 HTTP 요청 시나리오를 시뮬레이션**
4. **독립적이고 반복 실행 가능한 테스트 작성**
5. **실패 시 명확한 원인을 파악할 수 있도록 assert 및 메시지 작성**

### [중요] FastAPI 스키마 분리 및 테스트 작성 규칙
- 모든 POST/PUT 테스트는 반드시 `json=...`으로 요청해야 하며, `data=...`(폼 방식)는 사용 금지
- 엔드포인트는 Request/Response 스키마가 분리되어 있으므로, 테스트 입력도 별도 Request 스키마 구조를 따라야 함
- API 스키마가 변경될 경우 테스트 코드도 반드시 동기화 필요
- 테스트 실패 시 Pydantic ValidationError(특히 id 필드 누락 등)는 대부분 잘못된 요청 스키마/응답 구조에서 발생하므로, 엔드포인트와 테스트가 일치하는지 확인할 것

### [예시] 최신 CRUD 테스트 코드 (User)
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    resp = client.post("/api/v1/users/users/", json={
        "username": "alice", "email": "alice@example.com", "full_name": "Alice", "password": "testpw", "disabled": False
    })
    assert resp.status_code == 200
    assert resp.json()["username"] == "alice"

# ... (get/update/delete 등도 동일하게 json=... 사용)
```

### [예시] 주석/문서화 스타일
- 각 함수 상단에 한글 docstring으로 목적, 입력, 기대 결과 명시
- 주요 assert, 데이터 준비, 요청 부분에 한글 주석 추가

---

## docs/ 폴더 내 문서 안내
- [api_overview.md]: 전체 API 구조 및 엔드포인트 설명
- [connector_standard.md]: 커넥터 표준 및 확장 가이드
- [test_guide.md]: (이 문서) 테스트 작성/실행 가이드

---

## 테스트 실행 방법

1. **의존성 설치**
   - uv 환경 사용 시:
     ```bash
     uv pip install -r requirements.txt
     uv pip install pytest
     ```
   - 일반 가상환경 사용 시:
     ```bash
     pip install -r requirements.txt
     pip install pytest
     ```

2. **테스트 실행**
   - 전체 테스트 실행:
     ```bash
     pytest -v
     ```
   - 특정 테스트만 실행:
     ```bash
     pytest tests/user/test_user_crud.py
     ```

---

## 주요 테스트 케이스 설명

- **auth/test_auth.py**: 로그인 성공/실패 케이스 검증
- **user/test_user_crud.py**: 사용자 생성, 조회, 수정, 삭제, 리스트 조회
- **item/test_item_crud.py**: 아이템 생성, 조회, 수정, 삭제
- **common/test_health.py**: 서버 헬스체크
- **common/test_routes.py**: FastAPI에 실제 등록된 엔드포인트 목록 출력

---

## 테스트 관련 참고사항

- 모든 테스트는 FastAPI의 TestClient를 활용합니다.
- 테스트 실행 전, 환경변수(.env) 및 DB 설정이 필요할 수 있습니다.
- 테스트 코드에는 상세한 주석과 docstring이 포함되어 있어 이해와 유지보수가 용이합니다.
