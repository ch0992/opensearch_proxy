# FileDepot: 파일 업로드 서비스 기반 플랫폼

FileDepot은 다양한 외부 시스템 연동을 위한 커넥터 표준과, 실전 서비스 개발에 필요한 도메인 구조/예제를 제공합니다.

- **핵심 목표**: 커넥터와 표준화된 서비스 구조를 바탕으로, 개발자가 파일 업로드/관리 등 실전 서비스를 손쉽게 구현할 수 있도록 지원
- **커넥터**: Kafka, Oracle, MinIO, CUDU 등 외부 시스템 연동을 위한 Python 커넥터를 일부 제공 (FileDepot의 핵심이 아닌, 선택적 기능)
- **플랫폼 역할**: FileDepot 자체가 파일 업로드/관리 API를 제공하는 것이 아니라, 개발자가 이 플랫폼 구조와 커넥터를 활용해 직접 구현할 수 있도록 기반을 제공
- **도메인 구조**: 인증, 사용자, 아이템 등 실전 서비스에서 바로 활용 가능한 도메인 예제 및 표준 코드 포함

즉, FileDepot은 커넥터와 서비스 구조를 표준화하여, 파일 업로드/관리 등 다양한 비즈니스 서비스 개발을 빠르고 일관성 있게 할 수 있도록 돕는 플랫폼입니다.

---

## 주요 폴더/파일 구조

```
FileDepot/
  app/
    connectors/         # 외부 시스템 연동 커넥터 (Kafka, Oracle, CUDU, MinIO)
      kafka/producer.py
      kafka/consumer.py
      oracle.py
      cudu.py
      minio.py
    core/               # 공통 환경설정(config.py), 보안 유틸(security.py)
    domain/             # 도메인별 모델/서비스 (auth, user, item)
      auth/
      user/
      item/
    api/                # FastAPI 엔드포인트 (v1)
      v1/api.py
      v1/endpoints/
    docs/               # 📚 프로젝트 문서 및 가이드
      api_overview.md
      connector_standard.md
      test_guide.md
  tests/                # 도메인별/기능별 테스트 코드
    auth/
    user/
    item/
    common/
    conftest.py
  requirements.txt      # Python 의존성 명세
  README.md             # 프로젝트 설명서 (이 파일)
  .gitignore            # git 추적 제외 파일
```

---

## 📚 문서 리스트 (docs/)

- [docs/api_overview.md](app/docs/api_overview.md): API 구조 및 주요 엔드포인트 설명
- [docs/connector_standard.md](app/docs/connector_standard.md): 커넥터 표준 및 확장 가이드
- [docs/test_guide.md](app/docs/test_guide.md): 테스트 구조, 작성/실행 가이드, 예시 코드

---

## 커넥터 구조
- Kafka, Oracle, MinIO, CUDU 등 외부 시스템 연동을 위한 커넥터 Python 모듈 제공
- 각 커넥터는 표준화된 인터페이스와 예제 코드 포함

## 도메인 구조
- 실전 서비스에서 바로 사용할 수 있는 인증(auth), 사용자(user), 아이템(item) 도메인 예시 구현
- 각 도메인은 models.py(데이터모델), service.py(비즈니스로직)로 분리

## API 구조
- FastAPI 기반 RESTful API
- 버전별 엔드포인트: `/api/v1/`
- 인증, 사용자, 아이템 등 도메인별 endpoint 분리 구현

---

## 개발 및 실행 방법

1. **의존성 설치**
   - uv 환경 사용 권장
   - 또는 일반 가상환경/로컬 pip 사용 가능
   ```bash
   uv pip install -r requirements.txt
   uv pip install pytest
   ```

2. **서버 실행**
   ```bash
   uvicorn app.main:app --reload
   ```
   - 기본 주소: http://127.0.0.1:8000
   - API 문서: http://127.0.0.1:8000/docs

3. **테스트 실행**
   - 전체 테스트:
     ```bash
     pytest -v
     ```
   - 테스트 작성 가이드 및 예시는 `app/docs/test_guide.md` 참고

---

## 기타
- 환경변수/비밀키 등은 `.env` 파일로 관리
- 불필요한 파일/폴더는 `.gitignore`에 등록되어 git에서 자동 제외
- 상세한 테스트/코딩 가이드는 `app/docs/test_guide.md` 파일 참고

---

## 테스트 안내

테스트에 관한 자세한 내용은 `app/docs/test_guide.md`를 참고하세요.

```
FileDepot/
  app/
    core/
      config.py         # 전역 환경설정, 비밀키, DB, CORS 등
      security.py       # JWT, 패스워드 해시 등 공통 보안 유틸
    domain/
      auth/
        models.py       # 인증/인가 관련 모델 (User, Token 등)
        service.py      # 인증 서비스 (JWT, 패스워드 검증 등)
      user/
        models.py       # User 도메인 모델
        service.py      # User CRUD 비즈니스 로직
      item/
        models.py       # Item 도메인 모델
        service.py      # Item CRUD 비즈니스 로직
    api/
      v1/
        api.py
        endpoints/
          auth.py       # 인증 엔드포인트 (로그인 등)
          users.py      # User CRUD 엔드포인트
          items.py      # Item CRUD 엔드포인트
    main.py
```

- 각 도메인별(models.py, service.py)로 완전히 분리되어 확장성과 유지보수성 우수
- core/config.py, security.py는 모든 도메인/서비스/엔드포인트에서 import해서 사용
- API 엔드포인트는 도메인 계층만 import해서 입출력/유효성검사만 담당

---

## 라이브러리/모듈 현황 및 용도별 설명

### 전체 라이브러리 및 버전 (requirements.txt 스타일, 설명 주석 포함)

```text
fastapi==0.68.2          # API 서버 프레임워크 (전체 서비스)
uvicorn==0.15.0          # ASGI 서버 (FastAPI 실행)
passlib[bcrypt]==1.7.4   # 패스워드 해시/검증 (bcrypt 엔진, 인증/보안)
bcrypt==4.0.1            # bcrypt 엔진(버전 고정, passlib 내부에서 사용)
python-jose[cryptography]==3.4.0 # JWT 토큰 생성/검증 (인증/보안)
pydantic==1.10.21        # 데이터 검증/직렬화 (모델, 전체 서비스)
SQLAlchemy==2.0.38       # ORM, DB 연동 (user, item 도메인 등)
python-multipart==0.0.9  # 폼 데이터 파싱 (파일 업로드 등)
email-validator==2.1.1   # 이메일 형식 검증
starlette==0.14.2        # FastAPI 내부 의존성 (미들웨어 등)
requests==2.26.0         # HTTP API 연동 (CUDU, 외부 API)
minio==7.1.14            # MinIO S3 커넥터
oracledb==1.3.2          # Oracle DB 커넥터 (oracledb, cx_Oracle 대체)
faststream==0.5.39       # Kafka 커넥터 (producer/consumer)
aiokafka==0.12.0         # Kafka 비동기 클라이언트
python-dotenv==1.0.0     # 환경변수 관리 (core/config)
pytest==6.2.4            # 테스트
httpx==0.18.2            # API 테스트 클라이언트
emails==0.6              # 이메일 발송 유틸 (utils.py)
Jinja2==3.1.4            # 이메일 템플릿 등
```

---

### 용도별/도메인별 라이브러리 분류 및 설명

#### [공통/서비스]
- **fastapi**: 전체 API 서버 프레임워크
- **uvicorn**: ASGI 서버 (FastAPI 실행)
- **starlette**: FastAPI 내부 미들웨어, CORS 등
- **pydantic**: 데이터 검증/직렬화 (모델)
- **python-multipart**: 파일 업로드/폼 데이터 파싱
- **email-validator**: 이메일 형식 검증
- **python-dotenv**: 환경변수 관리 (core/config)
- **emails, Jinja2**: 이메일 발송/템플릿 (utils.py)

#### [DB/ORM]
- **SQLAlchemy**: 관계형 DB 연동 (user, item 등)

#### [인증/보안]
- **python-jose[cryptography]**: JWT 토큰 생성/검증 (auth, core/security)
- **passlib[bcrypt]**, **bcrypt**: 패스워드 해시/검증 (core/security, auth)

#### [Kafka 커넥터]
- **faststream**: Kafka 프로듀서/컨슈머 (connectors/kafka/producer.py, consumer.py)
- **aiokafka**: Kafka 비동기 클라이언트 (필요시)

#### [MinIO 커넥터]
- **minio**: S3 호환 오브젝트 스토리지 연동 (connectors/minio.py)

#### [Oracle 커넥터]
- **oracledb**: Oracle DB 연동 (connectors/oracle.py)

#### [CUDU/HTTP 커넥터]
- **requests**: REST API 연동 (connectors/cudu.py, 예제)

#### [테스트/유틸]
- **pytest**: 테스트 프레임워크
- **httpx**: API 테스트 클라이언트

---

#### 도메인/커넥터별 라이브러리 요약
- **auth 도메인**: fastapi, python-jose, passlib, bcrypt, pydantic
- **user/item 도메인**: fastapi, pydantic, sqlalchemy, email-validator
- **core/config**: pydantic, python-dotenv (선택)
- **커넥터별**: faststream/aiokafka(Kafka), minio(MinIO), cx_Oracle(Oracle), requests(CUDU)

---

## 커넥터별/도메인별 주요 라이브러리 정리

### Kafka 커넥터
- `faststream`    # Kafka 프로듀서/컨슈머 (connectors/kafka/)
- `aiokafka`      # 비동기 Kafka 클라이언트 (필요시)

### MinIO 커넥터
- `minio`         # MinIO S3 호환 오브젝트 스토리지 연동

### Oracle 커넥터
- `cx_Oracle`     # Oracle DB 연동

### CUDU 커넥터 (예시)
- `requests`      # HTTP API 연동 (RESTful)

### 도메인별
- **auth**: fastapi, python-jose, passlib, bcrypt, pydantic
- **user/item**: fastapi, pydantic, sqlalchemy, email-validator
- **core/config**: pydantic, python-dotenv (선택)

---

## requirements.txt 예시 (주석 포함)

```text
fastapi==0.68.2          # API 서버 프레임워크
uvicorn==0.15.0          # ASGI 서버
passlib[bcrypt]==1.7.4   # 패스워드 해시/검증 (bcrypt 엔진)
bcrypt==4.0.1            # bcrypt 엔진(버전 고정)
python-jose[cryptography]==3.4.0 # JWT 토큰
pydantic==1.10.21        # 데이터 검증/직렬화
SQLAlchemy==2.0.38       # ORM, DB 연동
python-multipart==0.0.9  # 폼 데이터 파싱
email-validator==2.1.1   # 이메일 검증
# faststream==0.x.x      # Kafka 커넥터
# minio==7.x.x           # MinIO 커넥터
# cx_Oracle==8.x.x       # Oracle 커넥터
# requests==2.x.x        # HTTP API 연동
```

---

## 설치 및 실행 방법 (uv 권장)

1. uv 설치 (최초 1회)
   ```bash
   pip install uv
   # 또는
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```

2. 의존성 설치
   ```bash
   uv pip install -r requirements.txt
   # 또는 pyproject.toml 사용 시
   uv pip install
   ```

3. 개발 서버 실행 (예시)
   ```bash
   uvicorn app.main:app --reload
   ```

- 각 예제(example) 폴더별 실행법은 해당 docs.md 참고

## 개발/확장 가이드
- 도메인별 폴더 구조를 참고해 새로운 기능을 쉽게 추가/확장 가능
- 인증, 보안, DB, 커넥터 등은 core/domain 계층에서 집중 관리
- 실전 구조와 예제 구조의 차이, 확장 방법은 각 docs.md에서 안내
- 새로운 외부 시스템 연동이 필요하면 connectors/ 하위에 추가 구현
- 표준 커넥터를 직접 수정하지 않고, 인터페이스만 활용
- 상세 표준/가이드는 docs/connector_standard.md 참고

## 예시
- FastAPI에서 Kafka, MinIO 연동: examples/fastapi_example.py
- ETL 처리에서 Kafka, Oracle 연동: examples/etl_example.py

## 설치 방법

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
- `.env` 파일을 프로젝트 루트에 생성하고 필요한 설정을 입력

4. 데이터베이스 초기화:
```bash
python -m app.initial_data
```

## 실행 방법

개발 서버 실행:
```bash
uvicorn app.main:app --reload
```

서버가 시작되면 다음 URL에서 API를 확인할 수 있습니다:
- API 문서: http://localhost:8000/docs
- ReDoc 문서: http://localhost:8000/redoc

## API 엔드포인트

### 인증
- POST `/api/v1/login/access-token` - 액세스 토큰 획득
- POST `/api/v1/login/test-token` - 토큰 테스트

### 사용자
- GET `/api/v1/users/` - 사용자 목록 조회 (관리자 전용)
- POST `/api/v1/users/` - 새 사용자 생성 (관리자 전용)
- GET `/api/v1/users/me` - 현재 사용자 정보 조회
- PUT `/api/v1/users/me` - 현재 사용자 정보 수정
- GET `/api/v1/users/{user_id}` - 특정 사용자 조회

## 보안

- JWT 토큰 기반 인증
- 비밀번호 해싱
- CORS 보호
- 사용자 권한 관리
