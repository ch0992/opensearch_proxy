import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def fake_opensearch_metadata():
    return {
        "filename": "test.jpg",
        "size": 1234,
        "uploader": "admin@example.com",
        "uploaded_at": "2025-04-19T12:34:56Z"
    }

@patch("app.connectors.opensearch.OpenSearchConnector.get_file_metadata")
def test_get_file_metadata_success(mock_get_metadata, fake_opensearch_metadata):
    mock_get_metadata.return_value = fake_opensearch_metadata
    file_id = "test-file-id"
    resp = client.get(f"/api/v1/files/{file_id}")
    assert resp.status_code == 200
    assert resp.json()["filename"] == "test.jpg"
    assert resp.json()["uploader"] == "admin@example.com"

@patch("app.connectors.opensearch.OpenSearchConnector.get_file_metadata")
def test_get_file_metadata_not_found(mock_get_metadata):
    mock_get_metadata.return_value = None
    file_id = "not-exist"
    resp = client.get(f"/api/v1/files/{file_id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "파일 정보를 찾을 수 없습니다."
