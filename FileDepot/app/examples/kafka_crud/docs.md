# Kafka 커넥터 기반 CRUD Example API 가이드

이 예제는 FastStream 기반 Kafka 커넥터를 활용하여 메시지 기반 CRUD API를 구현하는 방법을 안내합니다.
메시지 발행/수신 구조와 FastAPI 연동 포인트를 단계별로 설명합니다.

---

## 1. 목적
- Kafka 커넥터를 활용해 메시지 기반 CRUD(생성, 조회, 수정, 삭제) API를 구현하는 방법을 익힙니다.
- 실제 DB 없이 메시지 발행/수신 구조에 집중합니다.

---

## 2. 전체 구조
```
main.py              # FastAPI 앱, Kafka 커넥터, CRUD 엔드포인트 구현
```

---

## 3. 단계별 구현 방법

### 1) Kafka 커넥터 인스턴스 생성
```python
from app.connectors.kafka.producer import KafkaProducer
from app.connectors.kafka.consumer import KafkaConsumer
kafka_producer = KafkaProducer(brokers=["localhost:9092"])
kafka_consumer = KafkaConsumer(brokers=["localhost:9092"], group_id="crud-group")
```

### 2) CRUD 메시지 발행 엔드포인트 구현
- **생성(Create)**: POST /items/ → "crud-create" 토픽으로 메시지 발행
- **수정(Update)**: PUT /items/{item_id} → "crud-update" 토픽으로 메시지 발행
- **삭제(Delete)**: DELETE /items/{item_id} → "crud-delete" 토픽으로 메시지 발행

### 3) Kafka 메시지 수신 핸들러 등록
```python
def handle_create(message): ...
def handle_update(message): ...
def handle_delete(message): ...

kafka_consumer.subscribe("crud-create", handle_create)
kafka_consumer.subscribe("crud-update", handle_update)
kafka_consumer.subscribe("crud-delete", handle_delete)
```

### 4) FastAPI 서버 시작 시 컨슈머 등록
```python
@app.on_event("startup")
def on_startup():
    start_kafka_consumers()
```

### 5) 메시지 기반 조회(Read) 구현
- 수신된 메시지를 메모리(received_items)에 저장, GET /items/{item_id}로 조회

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
3. Kafka 브로커가 실행 중이어야 합니다.
4. 터미널에서 아래 명령어로 실행
   ```bash
   uvicorn main:app --reload
   ```
5. Swagger UI(http://localhost:8000/docs)에서 엔드포인트 테스트

---

## 5. 확장/응용 팁
- 실제 서비스에서는 메시지 수신 후 DB/외부 시스템에 저장하도록 확장할 수 있습니다.
- Kafka 커넥터의 토픽/핸들러 구조를 참고해 다양한 이벤트 기반 API로 확장 가능합니다.
