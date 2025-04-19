# Kafka Installation Guide

## Overview
This guide explains how to install and test Apache Kafka using ArgoCD on a Kind cluster.

## Prerequisites
- Kind cluster running
- ArgoCD installed
- MetalLB configured (IP range: 172.19.255.200-172.19.255.250)

## Installation

### 1. Configuration Files
The Kafka installation uses the following configuration files:

#### application.yaml
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kafka
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/ch0992/opensearch_proxy.git
    targetRevision: HEAD
    path: Infra/argocd/kafka/helm
    helm:
      valueFiles:
      - values.yaml
      - values-custom.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: kafka
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

#### values-custom.yaml
Key configurations:
- Single controller node (replicaCount: 1)
- Resource limits:
  - CPU: 200m-500m
  - Memory: 512Mi-1Gi
- Heap settings: -Xms256m -Xmx512m
- Persistence enabled (1Gi)
- LoadBalancer service with MetalLB (172.19.255.201)

### 2. Deployment
```bash
# Deploy Kafka
kubectl apply -f infra/argocd/kafka/application.yaml
```

### 3. Verify Installation
```bash
# Check pods
kubectl get pods -n kafka

# Check services
kubectl get svc -n kafka
```

Expected services:
- kafka (ClusterIP)
- kafka-controller-0-external (LoadBalancer)
- kafka-controller-headless (ClusterIP)

## Testing

### 1. Create a Test Topic
```bash
kubectl exec -it -n kafka kafka-controller-0 -- kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 2. List Topics
```bash
kubectl exec -it -n kafka kafka-controller-0 -- kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 3. Produce Messages
```bash
kubectl exec -it -n kafka kafka-controller-0 -- bash -c 'echo "Hello Kafka" | kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092'
```

### 4. Consume Messages
```bash
kubectl exec -it -n kafka kafka-controller-0 -- kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092 --timeout-ms 5000 --max-messages 1
```

## Current Status
- Kafka cluster is running with 1 controller node
- Basic topic creation and producer operations are working
- Consumer operations need investigation (timeout issues observed)

## Next Steps
1. Investigate consumer timeout issues
2. Install Kafdrop for UI management
3. Configure proper monitoring
