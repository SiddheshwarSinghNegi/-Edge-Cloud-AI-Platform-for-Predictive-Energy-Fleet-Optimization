# Edge-Cloud AI Platform for Predictive Energy & Fleet Optimization

A production-style, portfolio-ready project that demonstrates an **edge–cloud** architecture for ingesting telemetry from EV chargers/batteries/grid sensors, running **transformer-based time-series** models for predictive maintenance & demand forecasting, and visualizing results with a **React + Grafana** dashboard.

> Local demo runs fully with Docker Compose (no AWS credentials needed). Terraform/ArgoCD manifests are provided for AWS & Kubernetes deployment.

## Highlights
- **Edge-Cloud Hybrid**: Minimal **edge simulator** publishes MQTT telemetry to a broker; cloud services ingest, store, and score.
- **ML Pipeline**: Transformer-based time-series training stubs, preprocessing, and model packaging for (mock) **SageMaker** endpoint.
- **APIs**: FastAPI services for telemetry ingest, device management, and prediction retrieval.
- **Observability**: Prometheus metrics and Grafana dashboards; logs and health endpoints.
- **CI/CD**: GitHub Actions pipelines (lint/test/build/publish) and **ArgoCD** app manifests for GitOps to EKS.
- **IaC**: Terraform stubs for AWS IoT Core, DynamoDB, S3, EKS, Lambda, and SageMaker endpoint placeholders.

## Architecture (Mermaid)
```mermaid
flowchart LR
  subgraph Edge
    ES[Edge Simulator (MQTT client)]
  end

  subgraph Cloud
    IOT[AWS IoT Core]
    ING[Ingest API (FastAPI)]
    FEAT[Preprocess/Feature]
    PRED[Inference API (FastAPI -> SageMaker)]
    DB[(DynamoDB)]
    S3[(S3 Raw/Batch)]
    UI[React + Grafana]
  end

  ES -- MQTT --> IOT
  IOT -- Rule/HTTP --> ING
  ING --> S3
  ING --> FEAT --> DB
  FEAT --> PRED --> DB
  PRED --> UI
  DB --> UI
```

## Run Locally (Docker Compose)
```bash
docker compose up --build
# Frontend:  http://localhost:5173
# Grafana:   http://localhost:3000  (admin/admin)
# Prometheus:http://localhost:9090
# APIs:
# - Ingest:  http://localhost:8081/docs
# - Devices: http://localhost:8082/docs
# - Predict: http://localhost:8083/docs
```

### Smoke Test
```bash
# Publish one telemetry event via Ingest API (simulates IoT rule HTTP integration)
curl -X POST http://localhost:8081/ingest \
  -H "content-type: application/json" \
  -d '{"device_id":"ev-001","ts": 1730457600,"voltage": 230.5,"current": 13.2,"temp":32.4,"status":"charging"}'

# Get latest predictions
curl http://localhost:8083/predictions/latest
```

## Deploy to AWS EKS + ArgoCD
1. **Build & push** images (GitHub Actions provided in `ci_cd/github-actions`).
2. **Provision** infra with Terraform under `infrastructure/terraform` (IoT Core, S3, DynamoDB, EKS, Lambda, SageMaker).
3. **Bootstrap ArgoCD**, then apply manifests under `ci_cd/argocd/`. ArgoCD will sync services to EKS (blue/green or rolling).

## Repo Layout
```
EdgeCloud-AI-Predictive-Platform/
  backend/          # FastAPI services & edge simulator
  frontend/         # React app (embeds Grafana)
  ml_models/        # Transformer time-series training/inference stubs
  infrastructure/   # Terraform & k8s manifests
  ci_cd/            # GitHub Actions & ArgoCD
  docs/             # Usage & API docs
  docker-compose.yaml
```
