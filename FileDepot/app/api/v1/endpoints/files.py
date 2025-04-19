from fastapi import APIRouter, HTTPException
from app.connectors.opensearch import OpenSearchConnector

router = APIRouter()

@router.get("/files/{file_id}", summary="파일 메타데이터 조회", tags=["files"])
def get_file_metadata(file_id: str):
    """
    파일 ID로 OpenSearch에서 메타데이터를 조회합니다.
    """
    opensearch = OpenSearchConnector()
    metadata = opensearch.get_file_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="파일 정보를 찾을 수 없습니다.")
    return metadata
