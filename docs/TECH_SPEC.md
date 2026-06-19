# TECH_SPEC.md
**Project:** creator‑craft  
**Owner:** AxentX – Product Engineering  
**Status:** Draft (ready for review)  
**Last Updated:** 2026‑06‑19  

---  

## Table of Contents
1. [Overview](#1-overview)  
2. [Goals & Success Metrics](#2-goals--success-metrics)  
3. [Architecture Overview](#3-architecture-overview)  
4. [Core Components](#4-core-components)  
5. [Data Model](#5-data-model)  
6. [Key APIs & Interfaces](#6-key-apis--interfaces)  
7. [Technology Stack](#7-technology-stack)  
8. [External Dependencies](#8-external-dependencies)  
9. [Deployment & Operations](#9-deployment--operations)  
10. [Security & Compliance](#10-security--compliance)  
11. [Observability & Monitoring](#11-observability--monitoring)  
12. [Scalability & Performance](#12-scalability--performance)  
13. [Testing Strategy](#13-testing-strategy)  
14. [Future Enhancements](#14-future-enhancements)  
15. [Appendix](#15-appendix)  

---  

## 1. Overview
**creator‑craft** is a **no‑code / low‑code** SaaS platform that empowers indie creators to design, prototype, and launch software products without writing code. Users assemble **modules** (e.g., authentication, payments, data storage, UI widgets) via a visual canvas, configure them through declarative JSON/YAML, and publish a fully‑hosted web app with a single click.

The platform is built on top of AxentX’s existing data pipelines (auto, messages, instr‑resp, query‑resp) and leverages the **vLLM** inference engine for AI‑assisted component generation and the **SGLang** structured generation framework for code suggestions.

---  

## 2. Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| Rapid product creation | Avg. time from “new project” to “publish” | ≤ 5 min |
| Low technical barrier | % of users with < 2 hrs of prior dev experience | ≥ 80 % |
| Platform reliability | 99.9 % uptime (monthly) | – |
| Revenue validation | Conversion from free trial to paid plan | ≥ 15 % |
| Ecosystem growth | Number of community‑contributed modules | ≥ 200 by Q4 2027 |

---  

## 3. Architecture Overview
```
+-------------------+       +-------------------+       +-------------------+
|   Front‑End UI    | <---> |   API Gateway     | <---> |   Auth Service    |
| (React + Vite)   |       | (FastAPI + OIDC)  |       +-------------------+
+-------------------+       +-------------------+                |
          |                         |                         |
          v                         v                         v
+-------------------+   +-------------------+   +-------------------+
|   Canvas Engine   |   |   Module Registry |   |   Billing Service |
| (React‑Flow)      |   | (PostgreSQL)      |   | (Stripe SDK)      |
+-------------------+   +-------------------+   +-------------------+
          |                         |                         |
          v                         v                         v
+---------------------------------------------------------------+
|                     Orchestration Layer                      |
|  (Celery + Redis) – handles async builds, AI‑assisted code   |
+---------------------------------------------------------------+
          |
          v
+-------------------+    +-------------------+    +-------------------+
|   Build Workers   |    |   Runtime Engine  |    |   Storage Service |
| (Docker + Buildx) |    | (vLLM + SGLang)   |    | (S3‑compatible)   |
+-------------------+    +-------------------+    +-------------------+
```

* **Front‑End UI** – React SPA with Vite, using **React‑Flow** for drag‑and‑drop canvas.  
* **API Gateway** – FastAPI (Python 3.11) exposing REST + WebSocket endpoints, protected by OIDC (Keycloak).  
* **Auth Service** – Centralized JWT issuance, role‑based access control (RBAC).  
* **Module Registry** – PostgreSQL 15 schema storing module definitions, versioning, and metadata.  
* **Orchestration Layer** – Celery workers (concurrency = auto‑scale) backed by Redis 7 for task queue.  
* **Build Workers** – Containerized build environment using Docker‑in‑Docker, leveraging **Buildx** for multi‑arch images.  
* **Runtime Engine** – Executes AI‑generated code snippets via **vLLM** (GPU‑accelerated) and **SGLang** for structured generation (e.g., form schemas).  
* **Storage Service** – Object storage (MinIO) for user assets, generated bundles, and logs.  

---  

## 4. Core Components  

| Component | Responsibility | Primary Language / Tech |
|-----------|----------------|--------------------------|
| **Canvas UI** | Visual composition, live preview | React, TypeScript, React‑Flow |
| **Module Registry API** | CRUD for modules, version control | FastAPI (Python) |
| **AI Assistant Service** | Suggest component code, auto‑fill configs | vLLM, SGLang, Python |
| **Build Orchestrator** | Queue builds, manage Docker images | Celery, Redis |
| **Builder** | Translate module graph → Docker image | Dockerfile templates, Buildx |
| **Runtime Host** | Serve generated apps (static + serverless functions) | Nginx + FastAPI (as edge functions) |
| **Billing & Subscription** | Plan enforcement, usage metering | Stripe SDK, PostgreSQL |
| **Observability** | Tracing, metrics, logs | OpenTelemetry, Prometheus, Grafana, Loki |

---  

## 5. Data Model  

### 5.1 PostgreSQL Schema (simplified)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_pw TEXT NOT NULL,
    role TEXT CHECK (role IN ('creator','admin')) DEFAULT 'creator',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY,
    owner_id UUID REFERENCES users(id),
    name TEXT NOT NULL,
    status TEXT CHECK (status IN ('draft','building','ready','failed')) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE modules (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    definition JSONB NOT NULL,        -- declarative spec (inputs, outputs)
    source_code TEXT,                 -- optional AI‑generated snippet
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE project_modules (
    project_id UUID REFERENCES projects(id),
    module_id UUID REFERENCES modules(id),
    position JSONB,                   -- x,y coordinates on canvas
    config JSONB,                     -- user overrides
    PRIMARY KEY (project_id, module_id)
);

CREATE TABLE builds (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    status TEXT CHECK (status IN ('queued','running','success','error')) DEFAULT 'queued',
    log_url TEXT,
    artifact_url TEXT,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ
);
```

### 5.2 Object Storage Layout (MinIO)

```
/creator-craft/
   users/{user_id}/avatars/
   projects/{project_id}/
       source/          <-- source files before build
       build/           <-- Docker image tarball, manifest.json
       logs/
```

---  

## 6. Key APIs & Interfaces  

### 6.1 Public REST API (prefix `/api/v1`)

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| POST | `/projects` | Create new project | `{name:string}` | `{id, name, status}` |
| GET | `/projects/{id}` | Retrieve project metadata | – | Project object |
| PATCH | `/projects/{id}` | Update name / status | `{name?}` | Updated object |
| POST | `/projects/{id}/modules` | Attach module to canvas | `{module_id, position, config}` | 201 |
| DELETE | `/projects/{id}/modules/{module_id}` | Detach module | – | 204 |
| POST | `/projects/{id}/build` | Trigger build | – | `{build_id}` |
| GET | `/builds/{build_id}` | Build status & logs | – | `{status, log_url, artifact_url}` |
| POST | `/ai/suggest` | AI‑assist module generation | `{prompt:string, context?:object}` | `{module_spec}` |

All endpoints require a Bearer JWT with `role=creator` or `admin`.

### 6.2 WebSocket (Live Preview)

- **Endpoint:** `wss://api.axentx.com/preview/{project_id}`
- **Messages:**  
  - `canvas_update` – payload: current module graph (JSON).  
  - `preview_ready` – payload: URL to temporary preview instance.  

### 6.3 Internal Interfaces  

| Interface | Producer | Consumer | Protocol |
|-----------|----------|----------|----------|
| `build_task` | API Gateway (enqueue) | Celery workers | Redis queue |
| `artifact_publish` | Builder | Runtime Host | HTTP POST (signed URL) |
| `usage_event` | Runtime Host | Billing Service | Kafka topic `usage.events` |

---  

## 7. Technology Stack  

| Layer | Technology | Version (as of 2026‑06) |
|-------|------------|--------------------------|
| Front‑End | React 18, TypeScript 5, Vite 5, React‑Flow 11 | |
| API | FastAPI 0.112, Python 3.11, Uvicorn 0.30 | |
| Auth | Keycloak 24 (OIDC) | |
| DB | PostgreSQL 15, SQLAlchemy 2.0 | |
| Queue | Redis 7, Celery 5.4 | |
| Build | Docker Engine 24, Buildx 0.12, Docker‑in‑Docker (DinD) | |
| AI | vLLM 0.4.2 (GPU‑A100), SGLang 0.2.1 | |
| Storage | MinIO 2024‑09‑23 (S3‑compatible) | |
| Observability | OpenTelemetry SDK, Prometheus 2.53, Grafana 11, Loki 3.2 | |
| CI/CD | GitHub Actions, Docker Hub (private) | |
| Infra | Kubernetes 1.30 (EKS), Helm 3.15, Terraform 1.9 | |

---  

## 8. External Dependencies  

| Dependency | Reason | License |
|------------|--------|---------|
| Stripe API | Payment processing & subscription management | Proprietary |
| Keycloak | Centralized identity & RBAC | Apache‑2.0 |
| vLLM (GitHub: vllm-project/vllm) | High‑throughput LLM inference for AI assistant | Apache‑2.0 |
| SGLang (GitHub: sgl-project/sglang) | Structured generation of code snippets | Apache‑2.0 |
| React‑Flow | Canvas graph UI | MIT |
| PostgreSQL | Relational data store | PostgreSQL License |

All third‑party libraries are listed in `requirements.txt` with exact versions.

---  

## 9. Deployment & Operations  

### 9.1 Kubernetes Manifest Overview (Helm chart `creator-craft`)  

- **Namespace:** `creator-craft`
- **Deployments:**  
  - `frontend` (replicas = 3, resources = 200Mi/CPU = 200m)  
  - `api-gateway` (replicas = 4, resources = 300Mi/CPU = 250m)  
  - `celery-worker` (replicas = auto‑scale 2‑10, resources = 500Mi/CPU = 500m)  
  - `builder` (Job template, max‑concurrency = 5)  
  - `runtime-host` (replicas = 3, resources = 250Mi/CPU = 250m)  
- **StatefulSets:** `postgresql`, `redis`, `minio` (with PVCs)  
- **Ingress:** AWS ALB (TLS via ACM) routing `/api/*` → `api-gateway`, `/*` → `frontend`  
- **ConfigMaps/Secrets:**  
  - `app-config` (feature flags, AI model IDs)  
  - `db-credentials`, `redis-password`, `minio-access` (KMS‑encrypted)  

### 9.2 CI/CD Pipeline  

1. **Push → PR** – Lint (ESLint, flake8), unit tests, type checks.  
2. **Merge** – GitHub Actions builds Docker images, pushes to private ECR.  
3. **Helm Release** – `helm upgrade --install creator-craft ./helm` targeting `staging` then `prod`.  
4. **Canary** – 5 % traffic to new version, automated smoke tests via Postman collection.  

### 9.3 Disaster Recovery  

- **PostgreSQL** – Automated daily snapshots, point‑in‑time recovery (PITR) via AWS RDS.  
- **MinIO** – Replicated across three AZs, versioned objects.  
- **Redis** – AOF persistence + replica set.  

---  

## 10. Security & Compliance  

| Area | Controls |
|------|----------|
| Authentication | OIDC via Keycloak, MFA optional for admins |
| Authorization | RBAC enforced at API gateway; module‑level permissions |
| Data at Rest | PostgreSQL TLS, MinIO SSE‑S3, Redis TLS |
| Data in Transit | All endpoints HTTPS (TLS 1.3) |
| Secrets Management | AWS KMS + GitHub Secrets, never stored in repo |
| Auditing | Immutable audit log in CloudWatch (structured JSON) |
| GDPR/CCPA | User data export/delete endpoints, data retention policies (90 days for logs) |
| Pen‑Test | Quarterly external penetration test, automated OWASP ZAP scans in CI |

---  

## 11. Observability & Monitoring  

- **Metrics:** Prometheus exporters for FastAPI, Celery, Redis, PostgreSQL.  
- **Traces:** OpenTelemetry (trace propagation across HTTP, Celery, Docker builds).  
- **Logs:** Structured JSON logs shipped to Loki; retention 30 days (standard) / 90 days (premium).  
- **Dashboards:** Grafana dashboards for:  
  - Build queue latency  
  - AI assistant request latency & token usage  
  - User sign‑ups & conversion funnel  
- **Alerting:** PagerDuty alerts on:  
  - API error rate > 1 %  
  - Build failure rate > 5 %  
  - CPU > 80 % on any node for > 5 min  

---  

## 12. Scalability & Performance  

| Metric | Target | Test Method |
|--------|--------|-------------|
| Concurrent builds | 200 simultaneous | Load test with Locust (10 min ramp) |
| AI assistant latency | ≤ 800 ms 95th pct | Benchmark vLLM on A100 (batch = 8) |
| UI response time | ≤ 200 ms (SPA) | Lighthouse CI |
| Storage throughput | ≥ 5 GB/s aggregated | MinIO benchmark (mc admin speedtest) |
| Autoscaling | Horizontal pod autoscaler (CPU > 70 %) | K8s HPA policies |

---  

## 13. Testing Strategy  

- **Unit Tests:** Pytest (≥ 90 % coverage) for backend, Jest (≥ 85 %) for frontend.  
- **Integration Tests:** Docker‑compose environment exercising API ↔ DB ↔ Redis ↔ MinIO.  
- **End‑to‑End Tests:** Cypress covering user flows (project creation → build → publish).  
- **Performance Tests:** Locust scripts for API load, custom vLLM benchmark suite.  
- **Security Tests:** OWASP ZAP baseline scan, secret detection (GitLeaks) in CI.  

All tests run on every PR; blocking on failures.

---  

## 14. Future Enhancements  

1. **Marketplace** – Community‑driven module store with revenue sharing.  
2. **Multi‑tenant Runtime** – Isolated Kubernetes namespaces per published app.  
3. **Edge Functions** – Serverless function support via Cloudflare Workers integration.  
4. **AI Model Customization** – Fine‑tune vLLM on creator‑specific corpora (e.g., game dev prompts).  
5. **Collaboration** – Real‑time multi‑user canvas editing (CRDT‑based).  

---  

## 15. Appendix  

### 15.1 Environment Variables  

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | `development` | `production` | |
| `POSTGRES_URL` | PostgreSQL DSN | – |
| `REDIS_URL` | Redis connection string | – |
| `MINIO_ENDPOINT` | MinIO host | – |
| `STRIPE_SECRET_KEY` | Stripe API secret | – |
| `KEYCLOAK_URL` | OIDC issuer URL | – |
| `VLLM_MODEL_ID` | Identifier of LLM model in vLLM | `meta-llama/Meta-Llama-3.1-70B-Instruct` |
| `SGLANG_CONFIG` | Path to SGLang config JSON | `./config/sglang.json` |

### 15.2 Helm Values (excerpt)

```yaml
replicaCount: 3
image:
  repository: 123456789012.dkr.ecr.us-east-1.amazonaws.com/creator-craft
  tag: "{{ .Chart.AppVersion }}"
resources:
  limits:
    cpu: "500m"
    memory: "512Mi"
  requests:
    cpu: "250m"
    memory: "256Mi"
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

---  

*Prepared by:* Senior Product/Engineering Lead – AxentX  
*Reviewers:* Architecture Review Board, Security Team, QA Lead*
