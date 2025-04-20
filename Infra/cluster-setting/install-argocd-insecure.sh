#!/bin/bash
set -e

# 1. Install ArgoCD (latest stable)
echo "[1/4] Installing ArgoCD..."
kubectl create namespace argocd || true
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Patch ArgoCD server service to NodePort (insecure)
echo "[2/4] Patching ArgoCD server service to NodePort (insecure)..."
kubectl patch svc argocd-server -n argocd \
  -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 8080, "nodePort": 30080, "protocol": "TCP", "name": "http"}]}}' || true

# 3. Patch ArgoCD server deployment to allow insecure (disable TLS)
echo "[3/4] Patching ArgoCD server deployment for insecure (disable TLS)..."
kubectl patch deployment argocd-server -n argocd \
  --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--insecure"}]' || true

# 4. Port-forward for ArgoCD UI (background)
echo "[4/4] Port-forwarding ArgoCD UI to localhost:8090..."
nohup kubectl port-forward svc/argocd-server -n argocd 8090:80 > /dev/null 2>&1 &
echo "ArgoCD UI is now available at http://localhost:8090 (insecure)"

# 5. Wait for all ArgoCD pods to be ready, then print admin password
READY_PODS=0
REQUIRED_PODS=7
MAX_WAIT=120 # seconds
WAITED=0

# Wait until all pods are Running or Completed
while true; do
  READY_PODS=$(kubectl get pods -n argocd --no-headers | grep -E '(Running|Completed)' | wc -l)
  TOTAL_PODS=$(kubectl get pods -n argocd --no-headers | wc -l)
  if [ "$TOTAL_PODS" -ge "$REQUIRED_PODS" ] && [ "$READY_PODS" -eq "$REQUIRED_PODS" ]; then
    break
  fi
  if [ "$WAITED" -ge "$MAX_WAIT" ]; then
    echo "[WARN] Timeout waiting for ArgoCD pods to be ready."
    break
  fi
  echo "[INFO] Waiting for ArgoCD pods to be ready... ($WAITED/$MAX_WAIT sec)"
  sleep 5
  WAITED=$((WAITED+5))
done

# Print admin password
if kubectl -n argocd get secret argocd-initial-admin-secret >/dev/null 2>&1; then
  echo "[INFO] ArgoCD admin password (use this to login as 'admin'):"
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode; echo
else
  echo "[ERROR] Could not find argocd-initial-admin-secret. Please check pod status manually."
fi
