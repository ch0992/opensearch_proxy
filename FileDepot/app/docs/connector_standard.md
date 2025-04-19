# FileDepot Connector 표준 가이드

## 목적
- Kafka(FastStream), Oracle, CUDU, MinIO 등 외부 시스템 연동을 위한 "커넥터 표준"을 제공합니다.
- 실제 서비스 개발자는 이 커넥터 표준을 import 하여 비즈니스 로직을 구현하면 됩니다.

## 구조
```
app/connectors/
  kafka/producer.py
  kafka/consumer.py
  oracle.py
  cudu.py
  minio.py
app/examples/
app/docs/
```

## 개발/확장 방법
- 커넥터를 직접 수정하지 않고, 표준 인터페이스만 import하여 사용합니다.
- 새로운 시스템 연동이 필요하면 connectors/ 하위에 추가 구현 후, 예제/문서/테스트를 반드시 함께 제공합니다.
- 모든 커넥터는 docs/connector_standard.md 및 test_guide.md의 가이드에 따라 문서화/테스트가 이루어져야 합니다.
- 실제 서비스 연동 시, docs/ 폴더의 문서를 참고해 커넥터 구조와 사용법을 파악할 수 있습니다.

## 예시
- FastAPI에서 Kafka, MinIO 연동: app/examples/fastapi_example.py 참고
- ETL 처리에서 Kafka, Oracle 연동: app/examples/etl_example.py 참고

## 문서/테스트 정책
- 새 커넥터 추가 시 반드시 관련 문서(docs/)와 테스트(tests/)를 작성해야 하며, 기존 표준을 참고하여 일관된 구조로 유지합니다.
- 자세한 가이드: docs/connector_standard.md, docs/test_guide.md
