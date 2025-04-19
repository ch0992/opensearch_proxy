"""
app/connectors/oracle.py
- Oracle DB 연동 커넥터 표준 인터페이스 및 샘플 구현
- 실제 DB 연결/쿼리만 담당, 비즈니스 로직 없음
"""

import oracledb

class OracleConnector:
    def __init__(self, dsn: str, user: str, password: str):
        self.dsn = dsn
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        self.conn = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)

    def save_metadata(self, table: str, metadata: dict):
        """
        메타데이터를 지정 테이블에 저장 (예시)
        """
        if self.conn is None:
            self.connect()
        cursor = self.conn.cursor()
        cols = ', '.join(metadata.keys())
        vals = ', '.join([f":{k}" for k in metadata.keys()])
        sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
        cursor.execute(sql, metadata)
        self.conn.commit()
        cursor.close()
