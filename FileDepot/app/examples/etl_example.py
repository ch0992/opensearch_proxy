"""
app/examples/etl_example.py
- 커넥터 표준을 활용한 ETL 처리 예시
- 실제 서비스 개발자가 참고할 샘플
"""

from app.connectors.kafka.consumer import KafkaConsumer
from app.connectors.oracle import OracleConnector

# Kafka 컨슈머와 Oracle 커넥터 인스턴스 생성 예시
kafka_consumer = KafkaConsumer(brokers=["localhost:9092"], group_id="etl-group")
oracle_connector = OracleConnector(dsn="mydb_high", user="admin", password="password")

def handle_message(message):
    # 메시지를 받아 Oracle에 저장 (예시)
    oracle_connector.save_metadata("events", message)

# 토픽 구독 및 메시지 핸들러 등록
kafka_consumer.subscribe("events", handle_message)
