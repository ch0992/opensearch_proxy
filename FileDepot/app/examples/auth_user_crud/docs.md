# 인증 & User CRUD & Core Config/Security 예제 가이드

이 문서는 실전 서비스에서 자주 사용되는 인증(JWT, 패스워드 해시), User CRUD, core/config, security의 구조와 예제 코드를 FileDepot 도메인 기반 표준에 맞춰 정리합니다.

---

## 1. 목적
- 인증/인가(JWT, 패스워드 해시 등)와 User CRUD의 실전 구조와 예제를 한눈에 파악
- core/config, security 등 공통 유틸의 활용법까지 명확히 안내

---

## 2. 전체 폴더/파일 구조
```
app/
  core/
    config.py         # 환경설정, 비밀키, DB, CORS 등
    security.py       # JWT, 패스워드 해시 등 공통 보안 유틸
  domain/
    auth/
      models.py       # 인증/인가 관련 모델 (User, Token 등)
      service.py      # 인증 서비스 (JWT, 패스워드 검증 등)
    user/
      models.py       # User 도메인 모델
      service.py      # User CRUD 비즈니스 로직
  api/
    v1/
      endpoints/
        auth.py       # 인증 엔드포인트 (로그인 등)
        users.py      # User CRUD 엔드포인트
main.py
```

---

## 3. 핵심 기능별 예제 코드

### 1) core/config.py
- 환경설정, 비밀키, DB, CORS 등 전역 관리
- Pydantic BaseSettings로 .env, 환경변수 자동 로드

### 2) core/security.py
- JWT 토큰 생성/검증, 패스워드 해시/검증 함수 제공
- settings.SECRET_KEY 등 config.py의 설정값 활용

### 3) domain/auth/
- 인증 관련 모델(Token, UserInDB 등)과 서비스(JWT 발급, 패스워드 검증 등)
- 예시: 로그인 시 패스워드 검증, JWT 발급

### 4) domain/user/
- User 도메인 모델, CRUD 비즈니스 로직
- 임시 메모리 DB 예제 (실전에서는 DB 연동)

### 5) api/v1/endpoints/
- auth.py: 로그인 등 인증 엔드포인트
- users.py: User CRUD 엔드포인트

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
3. 개발 서버 실행
   ```bash
   uvicorn app.main:app --reload
   ```
4. Swagger UI(http://localhost:8000/docs)에서 로그인, User CRUD 등 테스트

---

## 5. 확장/실전 적용 팁
- DB 연동, OAuth2 커스텀, 권한 관리 등도 동일 구조에서 손쉽게 확장 가능
- 각 도메인별로 models.py, service.py, 엔드포인트를 분리 관리
- core/config, security는 모든 도메인/엔드포인트에서 import해서 재사용

### 5-1) 실전 DB 연동 예시
- User CRUD에서 임시 메모리 DB 대신 SQLAlchemy 등 ORM을 활용해 실제 DB와 연동
- 예시:
  ```python
  # domain/user/service.py
  from sqlalchemy.orm import Session
  from .models import UserDBModel

  def create_user(db: Session, user: UserCreate):
      db_user = UserDBModel(**user.dict())
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return db_user
  ```

### 5-2) OAuth2 커스텀/확장 예시
- OAuth2PasswordBearer, JWT 커스텀 클레임, refresh token 등도 core/security.py, domain/auth/service.py에서 확장 가능
- 예시:
  ```python
  # core/security.py
  def create_access_token(subject: str, scopes: List[str] = [], ...):
      to_encode = {"sub": subject, "scopes": scopes, ...}
      ...
  ```

### 5-3) 권한(Role) 관리 예시
- User 모델에 role 필드 추가, 엔드포인트에서 Depends로 권한 체크
- 예시:
  ```python
  # domain/user/models.py
  class User(BaseModel):
      ...
      role: str = "user"  # 예: "admin", "user"

  # endpoints/users.py
  from fastapi import Depends
  def admin_only(current_user: User = Depends(get_current_user)):
      if current_user.role != "admin":
          raise HTTPException(status_code=403, detail="권한 없음")
  ```

---

## 6. 참고
- 실전 구조/코드 예시는 app/domain, app/core, app/api/v1/endpoints 폴더에서 직접 확인
- 추가 확장/문서화가 필요하면 언제든 요청 가능
