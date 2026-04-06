# Clinic Management System — Lab 6 (Kubernetes Orchestration)

Повноцінна мікросервісна архітектура для управління клінікою, мігрована з Docker Compose під управління **Kubernetes**. Система побудована з використанням **FastAPI**, **PostgreSQL**, **Redis**, **Docker** та **Nginx**.

Ця (Шоста) лабораторна робота є логічним продовженням попередніх лаб: систему перенесено з `docker-compose` в локальний кластер Kubernetes (Docker Desktop), що забезпечило **автоматичне масштабування**, **відмовостійкість (self-healing)** та **плавні оновлення (rolling updates)**.

---

## 🏗️ Архітектура системи в Kubernetes

Система декомпозована на незалежні Pod'и, керовані через `Deployment`. Кожен має свій `Service` для внутрішнього DNS-based service discovery.

```
┌──────────────────────────────────────────────────────┐
│                 Kubernetes Cluster                    │
│                                                      │
│  ┌──────────┐     ┌──────────────────────────────┐   │
│  │  Nginx   │────▶│  patient-service (2 replicas) │  │
│  │ LBalancer│     └──────────────────────────────┘   │
│  │    :80   │     ┌──────────────────────────────┐   │
│  │          │────▶│  appointment-service          │   │
│  │          │     └──────────────────────────────┘   │
│  │          │     ┌──────────────────────────────┐   │
│  │          │────▶│  treatment-service            │   │
│  │          │     └──────────────────────────────┘   │
│  │          │     ┌──────────────────────────────┐   │
│  │          │────▶│  billing-service              │   │
│  └──────────┘     └──────────────────────────────┘   │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │ PG:Pats  │  │ PG:Appts │  │ PG:Treat │  │PG:Bil│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────┘ │
│                    ┌──────────┐                      │
│                    │  Redis   │                      │
│                    └──────────┘                      │
└──────────────────────────────────────────────────────┘
```

### Компоненти:
- **Patient Service** (2 репліки) — Управління даними пацієнтів та лікарів.
- **Appointment Service** — Планування візитів до лікарів.
- **Treatment Service** — Облік аналізів, діагнозів та планів лікування.
- **Billing Service** — Розрахунок вартості послуг та керування платежами.
- **API Gateway (Nginx)** — Єдина точка входу (`LoadBalancer :80`).
- **Redis Cache** — Глобальне in-memory сховище.
- **4× PostgreSQL** — Ізольовані бази даних для кожного сервісу (`Database-per-service pattern`).

---

## 🚀 Що нового у Лабораторній №6: Kubernetes

### Docker Compose → Kubernetes

| Можливість | Docker Compose | Kubernetes |
|---|---|---|
| **Масштабування** | Ручне (`docker-compose up --scale`) | Декларативне (`replicas: N`, `kubectl scale`) |
| **Відмовостійкість** | Контейнер падає — треба піднімати | Self-healing: Pod автоматично перестворюється |
| **Оновлення** | Rebuild + restart (даунтайм) | Rolling Update без даунтайму |
| **Service Discovery** | Docker DNS | Kubernetes DNS + Services |
| **Зберігання даних** | Docker Volumes | PersistentVolumeClaim (PVC) |

### Kubernetes об'єкти, що використовуються:
- `Deployment` — декларативне управління Pod'ами
- `Service (ClusterIP)` — внутрішній DNS для зв'язку між сервісами
- `Service (NodePort/LoadBalancer)` — зовнішній доступ до Nginx Gateway
- `ConfigMap` — конфігурація Nginx без пересбірки образу
- `PersistentVolumeClaim` — персистентне зберігання даних PostgreSQL

---

## 📂 Структура K8s маніфестів

```
k8s/
├── postgres-patients-deployment.yaml       # PostgreSQL + Service + PVC (patients)
├── postgres-appointments-deployment.yaml   # PostgreSQL + Service + PVC (appointments)
├── postgres-treatment-deployment.yaml      # PostgreSQL + Service + PVC (treatment)
├── postgres-billing-deployment.yaml        # PostgreSQL + Service + PVC (billing)
├── redis-deployment.yaml                   # Redis + Service
├── patient-deployment.yaml                 # Patient Service (2 replicas) + Service
├── appointment-deployment.yaml             # Appointment Service + Service
├── treatment-deployment.yaml               # Treatment Service + Service
├── billing-deployment.yaml                 # Billing Service + Service
└── nginx-deployment.yaml                   # Nginx + ConfigMap + Service (LoadBalancer)
```

---

## ⚡ Швидкий старт

### 1. Збірка Docker-образів

Перед деплоєм потрібно зібрати образи локально (Kubernetes використовує `imagePullPolicy: Never`):

```bash
cd clinic_management
docker build -t patient-service:latest ./patient-service
docker build -t appointment-service:latest ./appointment-service
docker build -t treatment-service:latest ./treatment-service
docker build -t billing-service:latest ./billing-service
```

### 2. Деплой в Kubernetes

```bash
kubectl apply -f k8s/
```

### 3. Перевірка статусу

```bash
kubectl get pods
kubectl get services
```

### 4. Доступ до системи

Після успішного запуску система доступна за адресою: `http://localhost/`

---

## 🧪 Демонстрація можливостей Kubernetes

### 1. Масштабування (Scaling)
Збільшити кількість реплік `appointment-service` з 1 до 3:
```bash
kubectl scale deployment appointment-service --replicas=3
kubectl get pods -w
```

### 2. Відмовостійкість (Self-Healing)
Примусово видалити Pod — Deployment автоматично створить новий:
```bash
kubectl get pods
kubectl delete pod <pod-name>
kubectl get pods -w   # Спостерігаємо відновлення
```

### 3. Плавне оновлення (Rolling Update)
Оновити образ `billing-service` без даунтайму:
```bash
kubectl set image deployment/billing-service billing-service=billing-service:v2
kubectl rollout status deployment/billing-service
```

---

## 🛠️ Технологічний стек

- **Backend:** Python + FastAPI, SQLAlchemy, Alembic, Pydantic
- **Databases:** PostgreSQL (Relational), Redis (In-memory Cache)
- **Infrastructure:** Docker, Kubernetes (Docker Desktop), Nginx
- **Orchestration:** Kubernetes Deployments, Services, ConfigMaps, PVCs
- **Communication:** HTTP Clients (`httpx`), Kubernetes DNS-based Service Discovery

---

## 📖 Документація API (Swagger UI)

Через Nginx API-роутинг на `http://localhost/`:

- 🧑‍⚕️ **Patient API:** [http://localhost/docs/patients/](http://localhost/docs/patients/)
- 📅 **Appointment API:** [http://localhost/docs/appointments/](http://localhost/docs/appointments/)
- 💊 **Treatment API:** [http://localhost/docs/treatments/](http://localhost/docs/treatments/)
- 💳 **Billing API:** [http://localhost/docs/billing/](http://localhost/docs/billing/)
