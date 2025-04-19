"""
MinIO S3 커넥터 기반 CRUD Example API
- MinioConnector를 활용한 파일 업로드/다운로드 예제
- 실제 MinIO 서버 연동이 필요하며, 구조와 연동 포인트에 집중
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from app.connectors.minio import MinioConnector

app = FastAPI()

# MinIO 커넥터 인스턴스 (실제 환경정보로 변경 필요)
from app.core.config import settings
minio = MinioConnector(endpoint=settings.MINIO_ENDPOINT, access_key=settings.MINIO_ACCESS_KEY, secret_key=settings.MINIO_SECRET_KEY)
BUCKET = settings.MINIO_BUCKET

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    """MinIO에 파일 업로드 (Create)"""
    try:
        # 파일을 임시 저장 후 업로드
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
        minio.upload_file(BUCKET, temp_path, file.filename)
        return {"result": "MinIO 업로드 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def get_presigned_url(filename: str):
    """MinIO presigned URL로 파일 다운로드 링크 제공 (Read)"""
    try:
        url = minio.get_presigned_url(BUCKET, filename)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
