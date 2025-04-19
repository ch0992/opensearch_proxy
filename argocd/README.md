# ArgoCD 배포 가이드

이 디렉토리는 OpenSearch와 Kafka의 ArgoCD 배포 구성을 포함하고 있습니다.

## 디렉토리 구조

```
argocd/
├── kafka/              # Kafka 배포 구성
│   ├── application.yaml   # ArgoCD Application 정의
│   └── helm/             # Kafka 헬름 차트
│       ├── Chart.yaml
│       └── values.yaml
└── opensearch/         # OpenSearch 배포 구성
    ├── application.yaml   # ArgoCD Application 정의
    └── helm/             # OpenSearch 헬름 차트
        ├── Chart.yaml
        └── values.yaml
```

## 배포 방법

### OpenSearch 배포

1. OpenSearch Application 배포
   ```bash
   kubectl apply -f opensearch/application.yaml
   ```

2. 배포 상태 확인
   ```bash
   kubectl get applications -n argocd opensearch
   ```

### Kafka 배포

1. Kafka Application 배포
   ```bash
   kubectl apply -f kafka/application.yaml
   ```

2. 배포 상태 확인
   ```bash
   kubectl get applications -n argocd kafka
   ```

## 구성 설정

### OpenSearch 설정
- `opensearch/helm/values.yaml`에서 OpenSearch 클러스터 구성을 설정할 수 있습니다.
- 주요 설정:
  - 노드 수
  - 리소스 할당
  - 보안 설정
  - 스토리지 구성

### Kafka 설정
- `kafka/helm/values.yaml`에서 Kafka 클러스터 구성을 설정할 수 있습니다.
- 주요 설정:
  - 브로커 수
  - 토픽 구성
  - 리소스 할당
  - 보안 설정

## 모니터링

ArgoCD UI에서 각 애플리케이션의 상태를 모니터링할 수 있습니다:
1. ArgoCD UI 접속
2. Applications 메뉴에서 해당 애플리케이션 선택
3. 동기화 상태 및 리소스 상태 확인
