# FastAPI Advanced Boilerplate

고급 기능을 갖춘 FastAPI 보일러플레이트 프로젝트입니다.

## 주요 기능

- 📝 SQLAlchemy ORM
- 🔐 JWT 인증
- 🛡️ 안전한 패스워드 해싱
- 🏢 CORS 미들웨어
- 📨 이메일 유틸리티
- 👥 사용자 관리 (슈퍼유저 포함)
- 🔄 의존성 주입
- 🎯 타입 힌트 적용
- 📚 자동 API 문서화

## 프로젝트 구조

```
.
├── app
│   ├── api              # API 라우터
│   │   └── v1          # API v1 엔드포인트
│   ├── core            # 설정, 보안 등 핵심 기능
│   ├── crud            # CRUD 작업
│   ├── db              # 데이터베이스 설정
│   ├── models          # SQLAlchemy 모델
│   └── schemas         # Pydantic 모델
├── tests               # 테스트 코드
└── requirements.txt    # 프로젝트 의존성
```

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
