"""
app/connectors/cudu.py
- CUDU 연동 커넥터 표준 인터페이스 및 샘플 구현
- 실제 연동 로직만 담당, 비즈니스 로직 없음
"""

class CUDUConnector:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

    def save_metadata(self, metadata: dict):
        """
        메타데이터를 CUDU 시스템에 저장 (예시)
        """
        # 실제 연동 로직은 시스템 API에 맞게 구현 필요
        pass
