#!/bin/bash
# 빌드 & 푸시 스크립트: FileDepot Docker 이미지
# 항상 latest 태그로 빌드 & 푸시
# 사용법: ./build-image.sh

set -e

REGISTRY=localhost:5001
IMAGE_NAME="filedepot"
TAG=latest
FULL_IMAGE="$REGISTRY/$IMAGE_NAME:$TAG"

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

echo "[INFO] requirements.txt 최신화 (필요시)"
pip install --upgrade pip
pip install -r requirements.txt || true

echo "[INFO] Docker 이미지 빌드: $FULL_IMAGE"
docker build -t $FULL_IMAGE .

echo "[INFO] 로컬 레지스트리($REGISTRY)로 이미지 푸시"
docker push $FULL_IMAGE

echo "[INFO] 빌드 및 푸시 완료: $FULL_IMAGE"

# # ArgoCD 자동 로그인 및 Hard Sync 실행
# ARGOCD_SERVER="localhost:8090"
# APP_NAME="filedepot"
# ARGOCD_NAMESPACE="argocd"
# ARGOCD_USER="admin"

# # admin 비밀번호 자동 획득
# ARGOCD_PWD=$(kubectl -n $ARGOCD_NAMESPACE get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode)
# echo "[INFO] ArgoCD admin 패스워드: $ARGOCD_PWD"

# # 로그인
# echo "[INFO] ArgoCD 로그인: argocd login $ARGOCD_SERVER --username $ARGOCD_USER --insecure"
# argocd login $ARGOCD_SERVER --username $ARGOCD_USER --password "$ARGOCD_PWD" --insecure
# LOGIN_RESULT=$?
# if [ $LOGIN_RESULT -ne 0 ]; then
#   echo "[ERROR] ArgoCD 로그인 실패. 수동으로 로그인 후 다시 시도하세요."
#   exit 1
# fi

# # Hard Sync
# echo "[INFO] ArgoCD Hard Sync 실행: argocd app sync $APP_NAME --server $ARGOCD_SERVER --force"
# argocd app sync $APP_NAME --server $ARGOCD_SERVER --force
# SYNC_RESULT=$?
# if [ $SYNC_RESULT -eq 0 ]; then
#   echo "[INFO] ArgoCD Hard Sync 성공"
# else
#   echo "[WARN] ArgoCD Hard Sync 실패 (코드: $SYNC_RESULT)"
# fi

