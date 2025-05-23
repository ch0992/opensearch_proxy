"""
app/connectors/minio.py
- MinIO S3 연동 커넥터 표준 인터페이스 및 샘플 구현
- 실제 파일 업로드/다운로드만 담당, 비즈니스 로직 없음
"""

from minio import Minio

from app.core.config import settings
class MinioConnector:
    def __init__(self, endpoint: str = None, access_key: str = None, secret_key: str = None, secure: bool = True):
        endpoint = endpoint or settings.MINIO_ENDPOINT
        access_key = access_key or settings.MINIO_ACCESS_KEY
        secret_key = secret_key or settings.MINIO_SECRET_KEY
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def upload_file(self, bucket: str, file_path: str, object_name: str):
        """
        파일을 MinIO에 업로드 (예시)
        """
        self.client.fput_object(bucket, object_name, file_path)

    def get_presigned_url(self, bucket: str, object_name: str, expires: int = 3600):
        """
        presigned URL 생성 (예시)
        """
        return self.client.presigned_get_object(bucket, object_name, expires=expires)
