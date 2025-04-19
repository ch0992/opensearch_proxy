# OpenSearch Proxy Platform

이 프로젝트는 OpenSearch와 연동하여 데이터를 관리하고 검색하는 플랫폼입니다.

## 프로젝트 구조

```
opensearch_proxy/
├── FileDepot/           # FastAPI 기반의 파일 관리 및 업로드 서비스
├── argocd/             # ArgoCD 배포 설정
│   ├── kafka/         # Kafka 배포 구성
│   └── opensearch/    # OpenSearch 배포 구성
└── origins/           # 헬름 차트 원본
    ├── charts/        # 커스텀 차트
    │   ├── kafka/     # Kafka 차트
    │   └── opensearch/ # OpenSearch 차트
    └── values/        # 환경별 values 파일
```

## 주요 컴포넌트

### 1. FileDepot
- FastAPI 기반의 파일 관리 및 업로드 서비스
- 자세한 내용은 [FileDepot/README.md](FileDepot/README.md) 참조

### 2. ArgoCD 배포 구성
- Kafka와 OpenSearch의 ArgoCD 배포 설정
- 각 컴포넌트별 application.yaml 및 헬름 차트 구성 포함

### 3. 헬름 차트
- Kafka와 OpenSearch의 커스텀 헬름 차트
- 환경별 values 파일을 통한 구성 관리

## 개발 환경 설정

1. 저장소 클론
   ```bash
   git clone https://github.com/ch0992/opensearch_proxy.git
   cd opensearch_proxy
   ```

2. FileDepot 서비스 실행
   - FileDepot 디렉토리의 README.md 참조

3. ArgoCD 배포
   ```bash
   # OpenSearch 배포
   kubectl apply -f argocd/opensearch/application.yaml
   
   # Kafka 배포
   kubectl apply -f argocd/kafka/application.yaml
   ```

## 환경 구성

### 개발 환경
- Python 3.12+
- Kubernetes 1.28+
- ArgoCD 2.9+
- OpenSearch 2.11+
- Kafka 3.6+

### 설정 파일
- `.env`: 환경 변수 설정 (gitignore에 포함)
- `values/`: 환경별 헬름 차트 values 파일

## 문서
각 컴포넌트의 자세한 설정과 사용법은 해당 디렉토리의 README.md를 참조하세요:
- [FileDepot 서비스](FileDepot/README.md)
- [ArgoCD 배포 가이드](argocd/README.md)
- [헬름 차트 문서](origins/README.md)
