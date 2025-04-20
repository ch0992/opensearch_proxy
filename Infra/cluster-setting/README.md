
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

## MetalLB 설치 및 설정

Kind 환경에서 LoadBalancer 타입의 Kubernetes 서비스를 사용하기 위해 MetalLB를 설치합니다.

1. MetalLB 설치
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-native.yaml
   ```

2. CRD 설치 확인
   ```bash
   kubectl get crd | grep metallb
   ```

3. IPAddressPool 및 L2Advertisement 설정

   `infra/metallb-config.yaml` 파일을 생성하고 다음 내용을 추가합니다.

   ```yaml
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     name: first-pool
     namespace: metallb-system
   spec:
     addresses:
       - 172.19.255.200-172.19.255.250  # Docker 네트워크 범위 내에서 사용할 IP 범위

   ---
   apiVersion: metallb.io/v1beta1
   kind: L2Advertisement
   metadata:
     name: l2-advert
     namespace: metallb-system
   spec:
     ipAddressPools:
       - first-pool
   ```

   설정 적용:
   ```bash
   kubectl apply -f infra/metallb-config.yaml
   ```

4. Docker 네트워크 범위 확인 (선택)
   ```bash
   docker network inspect kind | grep Subnet
   ```

   예: `172.19.0.0/16` 이라면 `172.19.255.x`도 같은 서브넷에 포함됩니다.

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
- MetalLB의 IP 풀은 Docker 네트워크 범위 내에서 설정해야 하며, 충돌이 없도록 주의하세요
```
