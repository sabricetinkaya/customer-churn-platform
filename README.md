# 🚀 Customer Churn Risk Monitoring Platform

> 🚧 This project is actively under development. Monitoring (Prometheus & Grafana) and cloud deployment are planned in upcoming iterations.

An event-driven customer churn prediction platform built with **FastAPI**, **Kafka**, **PostgreSQL**, **Docker**, and **XGBoost**.

The system predicts customer churn probability in real time, stores prediction history, tracks risk transitions, and exposes REST APIs for customer monitoring.

---

# ✨ Features

- Customer Management API (FastAPI)
- Event-Driven Architecture (Kafka)
- Real-time Churn Prediction
- Prediction History Tracking
- Risk Level Monitoring
- PostgreSQL Persistence
- Dockerized Microservices
- XGBoost Machine Learning Model
- Automated CI/CD Pipeline (GitHub Actions & Pytest)

---

# ⚙️ Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Machine Learning | XGBoost |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Event Streaming | Apache Kafka |
| Containerization | Docker & Docker Compose |
| CI/CD & Testing | GitHub Actions, Pytest, Flake8 |
| Artifact Registry | Docker Hub |
| Monitoring | Prometheus |
| API Documentation | Swagger UI |

---

# 🔄 CI/CD & Quality Assurance

This platform features a fully automated **GitHub Actions CI/CD pipeline** triggered on every `push` or `pull_request` to the main branch.

Code Push ──► Code Quality (flake8) ──► Unit Tests (pytest) ──► Build & Push (Docker Hub)

1. **Static Code Analysis:** Enforces PEP 8 compliance using `flake8`.
2. **Automated Unit Testing:** Executes unit tests via `pytest` to guarantee system integrity prior to containerization.
3. **Automated Deployment Artifacts:** Builds multi-container Docker images and pushes them automatically to **Docker Hub**.

---

# 📂 Project Structure

```
customer-churn-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD Pipeline
├── data/
├── docs/
│   ├── images/
│   └── system-design.drawio
│
├── logs/
├── model_artifacts/
├── notebooks/
├── src/
│   ├── api/
│   ├── database/
│   ├── inference/
│   ├── kafka/
│   ├── services/
│   ├── training/
│   └── utils/
│
├── tests/                  # Pytest Unit Tests
│   ├── init.py
│   └── test_api.py
│
├── docker-compose.yml
├── Dockerfile
├── prometheus.yml
├── requirements.txt
├── README.md
└── .env.example
```

---

# 🚀 Getting Started

## Clone repository

```bash
git clone [https://github.com/sabricetinkaya/customer-churn-platform.git](https://github.com/sabricetinkaya/customer-churn-platform.git)
cd customer-churn-platform
```

---

## Create environment file

```bash
cp .env.example .env
```

Update the environment variables if necessary.

---
---

## Run Unit Tests Locally
```bash
pip install -r requirements.txt
pytest
```
---

## Start the project

```bash
docker compose up --build
```

---
## 📐 Architecture
The platform follows an event-driven microservice architecture.

The overall workflow is:

- Client sends customer data to the FastAPI service.
- Customer events are published to Kafka.
- Prediction Service consumes customer events and performs ML inference.
- Prediction results are published back to Kafka.
- Persistence Service stores customer snapshots and prediction history in PostgreSQL.
- REST endpoints retrieve the latest customer state and prediction history.

The following diagrams illustrate the architecture in detail.

### System Architecture

![System Architecture](docs/images/system-architecture.png)

---

### Docker Container Architecture

![Docker Container Architecture](docs/images/docker-container-architecture.png)

---

### Database ER Diagram

![Database ER Diagram](docs/images/database-er-diagram.png)

---

> Editable diagrams are available in `docs/system-design.drawio`.

---
## API Documentation

Swagger UI

```
http://localhost:8000/docs
```

OpenAPI

```
http://localhost:8000/openapi.json
```

---

# 📌 API Endpoints

## Create Customer

```
POST /customers
```

Example Request

```json
{
  "customer_id": 1015,
  "Age": 35,
  "Gender": "Male",
  "Tenure": 6,
  "Usage Frequency": 4,
  "Support Calls": 3,
  "Payment Delay": 8,
  "Subscription Type": "Standard",
  "Contract Length": "Annual",
  "Total Spend": 720.5,
  "Last Interaction": 12
}
```

---

## Get Customer

```
GET /customers/{customer_id}
```

Example Response

```json
{
  "customer_id": 1015,
  "age": 35,
  "gender": "Male",
  "tenure": 6,
  "usage_frequency": 4,
  "support_calls": 3,
  "payment_delay": 8,
  "subscription_type": "Standard",
  "contract_length": "Annual",
  "total_spend": 720.5,
  "last_interaction": 12,
  "current_prediction": false,
  "current_churn_probability": 0.0323,
  "current_risk_level": "LOW"
}
```

---

## Prediction History

```
GET /customers/{customer_id}/history
```

Returns every prediction made for the customer.

---

## Risk Alerts

```
GET /alerts/risk-increased
```

Returns customers whose risk level increased.

---

# 🧠 Machine Learning

Model:

- XGBoost Classifier

Pipeline:

- ColumnTransformer
- OneHotEncoder
- XGBoost

Outputs:

- Churn Probability
- Predicted Churn
- Risk Level

Risk Levels

| Probability | Risk |
|--------------|------|
| < 0.40 | LOW |
| 0.40 - 0.70 | MEDIUM |
| > 0.70 | HIGH |

---

# 📊 Event Flow

Customer Created

```
CustomerCreated
        │
        ▼
customer.events
        │
        ▼
Prediction Service
        │
        ▼
PredictionCreated
        │
        ▼
prediction.events
        │
        ▼
Persistence Service
        │
        ▼
PostgreSQL
```

---

# 🐳 Docker Services

The project currently runs the following Docker services:

- PostgreSQL
- ZooKeeper
- Kafka
- Customer API
- Prediction Service
- Persistence Service
- Database Initialization Service
- Kafka Topic Initialization Service

---

# 📈 Monitoring | Planned (Prometheus & Grafana)

Monitoring with Prometheus and Grafana is planned as the next phase of the project.

Planned features:

- Prometheus metrics collection
- Grafana dashboards
- API performance monitoring
- Kafka monitoring
- PostgreSQL monitoring

---

# 🔮 Future Improvements

- Integrate Prometheus metrics collection
- Build Grafana dashboards
- Kafka UI
- AWS RDS deployment
- Model Registry (MLflow)
- Authentication & Authorization (JWT)
- Batch prediction endpoint
- Model retraining pipeline
---

# 👨‍💻 Author

**sabricetinkaya**

Customer Churn Risk Monitoring Platform

Built with FastAPI, Kafka, PostgreSQL, Docker and XGBoost.