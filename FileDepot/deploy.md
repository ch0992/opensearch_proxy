# FileDepot 배포 및 운영 가이드 (`deploy.md`)

## 1. 개요
FileDepot는 FastAPI 기반의 파일 메타데이터 관리/저장 서비스입니다. 이 문서는 FileDepot의 도커 이미지 빌드, 레지스트리 푸시, Kubernetes/ArgoCD 배포 및 운영 자동화 방법을 정리합니다.

---

## 2. 주요 환경 및 의존성
- **Python**: 3.12
- **FastAPI**: API 서버
- **Kafka**: 메시지 브로커 (faststream, aiokafka)
- **MinIO**: S3 호환 오브젝트 스토리지
- **OpenSearch**: 메타데이터 검색/저장
- **ArgoCD**: GitOps 기반 Kubernetes 배포 자동화
- **Docker**: 이미지 빌드 및 레지스트리 관리

### 2.1 requirements.txt 주요 패키지
- fastapi, uvicorn, aiokafka, faststream, minio, opensearch-py 등

---

## 3. 배포 및 운영 절차

### 3.1 도커 이미지 빌드 및 푸시
1. **필수 환경 준비**
    - `requirements.txt` 최신화: 필요 패키지(특히 faststream, minio 등) 추가
    - `.env` 파일에 Kafka, MinIO, OpenSearch, DB 등 환경 변수 설정
2. **이미지 빌드 및 푸시**
    ```bash
    sh build-image.sh
    ```
    - requirements.txt 설치 → 도커 이미지 빌드 → 로컬 레지스트리(`localhost:5001`)로 푸시

### 3.2 Kubernetes/ArgoCD 배포
- ArgoCD를 통해 Helm 차트 기반으로 FileDepot를 배포/운영
- ArgoCD 앱 이름: `filedepot`
- Helm values 파일: `infra/argocd/filedepot/helm/values-custom.yaml` 등

#### 수동 동기화(하드 싱크)
- ArgoCD UI 또는 CLI에서 수동으로 sync 가능

### 3.3 ArgoCD CLI 접속 및 동기화 (옵션)
> **포트포워딩 자동화는 스크립트에 포함하지 않음**

1. 별도 터미널에서 포트포워딩 실행
    ```bash
    kubectl port-forward svc/argocd-server -n argocd 8090:80
    ```
2. ArgoCD 로그인
    ```bash
    ARGOCD_PWD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode)
    argocd login localhost:8090 --username admin --password "$ARGOCD_PWD" --insecure
    ```
3. 동기화(하드 싱크)
    ```bash
    argocd app sync filedepot --server localhost:8090 --force
    ```

---

## 4. 트러블슈팅 & 참고사항

### 4.1 포트포워딩 문제
- 포트포워딩이 끊기거나 연결이 안 될 경우:
    - argocd-server Pod/Service 상태 확인
    - 포트포워딩 로그(`tail -n 50 /tmp/argocd-portforward.log`) 확인
    - Pod가 Running/Ready 상태인지 점검

### 4.2 의존성 오류
- `ModuleNotFoundError: No module named 'faststream'` 등 발생 시:
    - requirements.txt에 누락된 패키지 추가 후 재설치/재빌드

### 4.3 기타
- 필요시 minio, oracledb 등 커넥터 패키지도 requirements.txt에 추가
- 운영 자동화 스크립트(`build-image.sh`)에는 포트포워딩 자동화 미포함(수동 실행 권장)

---

## 5. 주요 파일 구조

```
FileDepot/
├── app/               # FastAPI 서비스 코드
├── build-image.sh     # 빌드/푸시 자동화 스크립트
├── requirements.txt   # Python 의존성 목록
├── Dockerfile         # 도커 빌드 파일
├── .env               # 서비스 환경 변수
├── README.md
├── deploy.md          # (본 문서)
└── ...
```

---

## 6. 참고/추가 개선사항
- 포트포워딩 자동화, 에러 핸들링, 로그 개선 등은 필요시 스크립트에 추가 가능
- CI/CD 파이프라인(GitHub Actions 등) 연동도 가능
- 운영 중 문제 발생 시 로그/Pod 상태/서비스 상태 점검 필수

---

> **문의/이슈**: 추가적인 배포 자동화, 장애 대응, 커넥터 확장 등 필요시 언제든 문의 바랍니다.
