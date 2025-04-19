# FastAPI CRUD Example API 가이드

이 예제는 FastAPI를 활용한 가장 기본적인 CRUD API 구현 방법을 단계별로 안내합니다.
초보자도 쉽게 따라할 수 있도록 전체 흐름과 각 코드의 역할을 상세히 설명합니다.

---

## 1. 목적
- FastAPI의 기본 구조와 CRUD(생성, 조회, 수정, 삭제) API 작성법을 익힙니다.
- 복잡한 DB, 외부 연동 없이 메모리 내 임시 저장소(fake_db)만 사용합니다.

---

## 2. 전체 구조
```
main.py              # FastAPI 앱과 CRUD 엔드포인트 구현
```

---

## 3. 단계별 구현 방법

### 1) FastAPI 앱 생성
```python
from fastapi import FastAPI
app = FastAPI()
```

### 2) 데이터 모델(Pydantic) 정의
```python
from pydantic import BaseModel
class Item(BaseModel):
    id: int
    name: str
    description: str = ""
```

### 3) 임시 메모리 DB 준비
```python
fake_db = {}
```

### 4) CRUD 엔드포인트 구현
- **생성(Create)**: POST /items/
- **조회(Read)**: GET /items/{item_id}
- **수정(Update)**: PUT /items/{item_id}
- **삭제(Delete)**: DELETE /items/{item_id}

각 엔드포인트는 예외 처리와 반환값을 명확히 하여, 실전 서비스 개발에 쉽게 확장할 수 있습니다.

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
3. 터미널에서 아래 명령어로 실행
   ```bash
   uvicorn main:app --reload
   ```
4. 브라우저에서 http://localhost:8000/docs 접속 (Swagger UI 자동 생성)
5. 각 엔드포인트를 직접 테스트하며 동작을 확인

---

## 5. 실전 구조와의 차이 및 확장 팁

- 이 예제는 단일 파일(main.py)에 모든 구조(모델, 서비스, 엔드포인트, 앱)가 포함되어 있어 FastAPI CRUD의 전체 흐름을 한눈에 파악할 수 있습니다.
- 실전 서비스에서는 도메인별로 models.py, service.py, 엔드포인트를 분리하여 확장성과 유지보수성을 높입니다.
- 예시 실전 구조:
  ```
  app/
    core/
      config.py
      security.py
    domain/
      auth/
        models.py
        service.py
      user/
        models.py
        service.py
      item/
        models.py
        service.py
    api/
      v1/
        endpoints/
          auth.py
          users.py
          items.py
    main.py
  ```
- core/config.py, security.py는 모든 도메인/엔드포인트에서 import해서 사용
- 실전 구조와 표준화된 폴더 구조는 README.md, 각 도메인별 docs.md에서 참고

- 실제 서비스에서는 fake_db 대신 DB/커넥터를 사용할 수 있습니다.
- Pydantic 모델, 예외처리, 엔드포인트 설계 등은 모든 FastAPI 프로젝트의 기본 템플릿이 됩니다.
