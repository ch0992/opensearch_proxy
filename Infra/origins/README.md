# Helm Charts

이 디렉토리는 OpenSearch와 Kafka의 커스텀 헬름 차트를 포함하고 있습니다.

## 디렉토리 구조

```
origins/
├── charts/            # 커스텀 헬름 차트
│   ├── kafka/        # Kafka 차트
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   └── opensearch/   # OpenSearch 차트
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
└── values/           # 환경별 values 파일
    ├── dev/         # 개발 환경
    ├── staging/     # 스테이징 환경
    └── prod/        # 운영 환경
```

## 차트 설명

### OpenSearch 차트
- OpenSearch 클러스터 배포를 위한 커스텀 차트
- 주요 기능:
  - 멀티 노드 클러스터 구성
  - 보안 설정
  - 리소스 관리
  - 모니터링 설정

### Kafka 차트
- Kafka 클러스터 배포를 위한 커스텀 차트
- 주요 기능:
  - 브로커 구성
  - 토픽 자동 생성
  - 보안 설정
  - 리소스 관리

## 환경별 설정

각 환경별로 다른 설정을 적용하기 위해 `values/` 디렉토리 아래에 환경별 values 파일을 관리합니다:

### 개발 환경 (dev)
- 최소한의 리소스로 구성
- 디버깅 및 로깅 활성화
- 단일 노드 구성

### 스테이징 환경 (staging)
- 운영 환경과 유사한 구성
- 모니터링 활성화
- 축소된 리소스 구성

### 운영 환경 (prod)
- 고가용성 구성
- 리소스 최적화
- 보안 강화
- 모니터링 및 알림 구성

## 차트 사용법

1. 차트 의존성 업데이트
   ```bash
   helm dependency update charts/opensearch
   helm dependency update charts/kafka
   ```

2. 차트 템플릿 확인
   ```bash
   # OpenSearch
   helm template opensearch charts/opensearch -f values/dev/opensearch.yaml

   # Kafka
   helm template kafka charts/kafka -f values/dev/kafka.yaml
   ```

3. 차트 배포
   ```bash
   # OpenSearch
   helm install opensearch charts/opensearch -f values/dev/opensearch.yaml

   # Kafka
   helm install kafka charts/kafka -f values/dev/kafka.yaml
   ```

## 차트 업데이트

1. Chart.yaml 버전 업데이트
2. 변경사항 CHANGELOG.md에 기록
3. 템플릿 테스트
4. values.yaml 예제 업데이트
