# Kind Cluster 설정 가이드

이 디렉토리는 로컬 개발 환경의 Kind Cluster 설정 파일을 포함하고 있습니다.

## 현재 클러스터 구성

### 노드 구성
- 1개의 control-plane 노드
- 2개의 worker 노드

### 포트 매핑 (control-plane 노드)
- OpenSearch HTTP: 30000
- OpenSearch Transport: 30001
- Kafka: 30002
- Kafka Manager: 30003

### 스토리지
- StorageClass:
  - standard (기본)
  - hostpath
  - 프로비저너: rancher.io/local-path
- PersistentVolume:
  - OpenSearch: /var/lib/opensearch-data
  - Kafka: /var/lib/kafka-data

## 데이터 디렉토리 설정

1. 데이터 디렉토리 생성
   ```bash
   sudo mkdir -p /var/lib/opensearch-data /var/lib/kafka-data
   sudo chmod 777 /var/lib/opensearch-data /var/lib/kafka-data
   ```

2. PersistentVolume 생성
   ```bash
   kubectl apply -f infra/storage.yaml
   ```

## 클러스터 관리

1. 클러스터 상태 확인
   ```bash
   kind get clusters
   kubectl cluster-info
   kubectl get nodes -o wide
   ```

2. 스토리지 상태 확인
   ```bash
   kubectl get sc
   kubectl get pv
   ```

## 주의사항
- 데이터 디렉토리의 권한이 올바르게 설정되어 있는지 확인하세요
- 호스트 포트가 사용 가능한지 확인하세요
- 기존 클러스터 설정을 변경할 때는 주의가 필요합니다
