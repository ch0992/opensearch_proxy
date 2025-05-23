# CUDU 커넥터 기반 CRUD Example API 가이드

이 예제는 CUDUConnector를 활용해 CUDU 시스템에 데이터를 저장/조회하는 기본 구조를 안내합니다.
실제 CUDU 시스템 연동은 샘플 구조와 연동 포인트에 집중합니다.

---

## 1. 목적
- CUDU 커넥터를 활용해 메타데이터를 저장/조회하는 방법을 익힙니다.
- 실전 서비스에서 CUDU 연동 CRUD API의 기본 템플릿으로 활용할 수 있습니다.

---

## 2. 전체 구조
```
main.py              # FastAPI 앱, CUDU 커넥터, CRUD 엔드포인트 구현
```

---

## 3. 단계별 구현 방법

### 1) CUDU 커넥터 인스턴스 생성
```python
from app.connectors.cudu import CUDUConnector
cudu = CUDUConnector(endpoint="https://cudu.example.com", api_key="your_api_key")
```

### 2) 데이터 모델(Pydantic) 정의
```python
from pydantic import BaseModel
class Item(BaseModel):
    id: int
    name: str
    description: str = ""
```

### 3) CUDU 저장 엔드포인트 구현
- **생성(Create)**: POST /items/ → CUDU에 저장

### 4) CUDU 조회 엔드포인트 구현 (예시)
- **조회(Read)**: GET /items/{item_id}
- 실제 조회 로직은 시스템 API에 맞게 확장 필요

---

## 4. 실행 및 테스트
1. uv 설치 (최초 1회)
   ```bash
   pip install uv
   # 또는
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```
2. 의존성 설치
   ```bash
   uv pip install -r requirements.txt
   ```
3. CUDU 시스템이 연동 가능해야 합니다.
4. 터미널에서 아래 명령어로 실행
   ```bash
   uvicorn main:app --reload
   ```
5. Swagger UI(http://localhost:8000/docs)에서 엔드포인트 테스트

---

## 5. 확장/응용 팁
- 실제 서비스에서는 UPDATE/DELETE 등 다양한 연동 메서드 구현 필요
- 커넥터의 메서드 구조를 참고해 다양한 외부 시스템 연동 API로 확장할 수 있습니다.
