from opensearchpy import OpenSearch
from typing import Optional
import os

from app.core.config import settings
class OpenSearchConnector:
    def __init__(self):
        self.host = getattr(settings, "OPENSEARCH_HOST", "localhost")
        self.port = int(getattr(settings, "OPENSEARCH_PORT", 9200))
        self.index = getattr(settings, "OPENSEARCH_INDEX", "filedepot_metadata")
        self.client = OpenSearch(
            hosts=[{"host": self.host, "port": self.port}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
        )

    def get_file_metadata(self, file_id: str) -> Optional[dict]:
        try:
            res = self.client.get(index=self.index, id=file_id)
            return res["_source"]
        except Exception as e:
            return None
