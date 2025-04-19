# MinIO S3 커넥터 기반 CRUD Example API 가이드

이 예제는 MinioConnector를 활용해 MinIO S3에 파일을 업로드/다운로드하는 API 구현 방법을 안내합니다.
실제 MinIO 서버와 연동해야 하며, 구조와 연동 포인트에 집중합니다.

---

## 1. 목적
- MinIO 커넥터를 활용해 파일 업로드/다운로드 API를 구현하는 방법을 익힙니다.
- 실전 서비스에서 S3 호환 스토리지 연동의 기본 템플릿으로 활용할 수 있습니다.

---

## 2. 전체 구조
```
main.py              # FastAPI 앱, MinIO 커넥터, 파일 업로드/다운로드 엔드포인트 구현
```

---

## 3. 단계별 구현 방법

### 1) MinIO 커넥터 인스턴스 생성
```python
from app.connectors.minio import MinioConnector
minio = MinioConnector(endpoint="localhost:9000", access_key="minio", secret_key="minio123")
```

### 2) 파일 업로드 엔드포인트 구현
- **업로드(Create)**: POST /upload/ → MinIO에 파일 저장

### 3) presigned URL 다운로드 엔드포인트 구현
- **다운로드(Read)**: GET /download/{filename} → presigned URL 반환

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
3. MinIO 서버가 실행 중이어야 합니다.
4. 터미널에서 아래 명령어로 실행
   ```bash
   uvicorn main:app --reload
   ```
5. Swagger UI(http://localhost:8000/docs)에서 업로드/다운로드 테스트

---

## 5. 확장/응용 팁
- 실제 서비스에서는 presigned URL 만료시간, 권한 관리 등 다양한 옵션을 활용할 수 있습니다.
- 커넥터의 메서드 구조를 참고해 다양한 파일 처리 API로 확장할 수 있습니다.
