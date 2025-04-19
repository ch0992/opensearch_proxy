# API 구조 및 예시 목록 (최신)

FileDepot의 API는 도메인/기능별로 분리되어 있으며, 모든 엔드포인트는 최신 FastAPI/Pydantic 스키마 분리 정책을 따릅니다.

- **Swagger 문서 자동화:** http://localhost:8000/docs
- **ReDoc 문서:** http://localhost:8000/redoc
- **Request/Response 모델 분리:** 모든 엔드포인트는 별도의 Request/Response Pydantic 스키마를 사용, API 명세가 명확하게 문서화됩니다.
- **테스트/문서 구조:** docs/ 폴더 및 test_guide.md 참고

---

## Example: 인증 (Login)
- **경로**: `/api/v1/login`
- **설명**: 사용자 로그인을 위한 인증 토큰 발급 예시 (Read: 인증 정보 확인 및 토큰 발급)

---

## Example: 사용자(User) CRUD
- **경로**: `/api/v1/users/`, `/api/v1/users/{user_id}`
- **설명**: 사용자 생성, 조회(Read), 수정, 삭제 기능 예시
  - **조회(Read)**: 특정 사용자 정보 읽기, 전체 사용자 목록 조회 등

---

## Example: 아이템(Item) CRUD
- **경로**: `/api/v1/items/`, `/api/v1/items/{item_id}`
- **설명**: 아이템 생성, 조회(Read), 수정, 삭제 기능 예시
  - **조회(Read)**: 특정 아이템 정보 읽기, 전체 아이템 목록 조회 등

---

> 각 API는 "example" 폴더 및 도메인 구조를 참고해 직접 확장/변경하여 사용할 수 있습니다.
> 실제 서비스 적용 전, 예제 코드를 기반으로 필요한 기능/설명을 추가하는 것을 권장합니다.
