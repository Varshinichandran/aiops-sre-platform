# AI-Driven AIOps SRE Platform

An AI-powered Kubernetes monitoring and self-healing platform that detects CPU anomalies using machine learning and automatically remediates issues.

---

## Tech Stack

- Kubernetes
- Prometheus
- Grafana
- FastAPI
- Python
- Machine Learning (Isolation Forest)

---

## Architecture Diagram

![Architecture](architecture/aiops-architecture.png)

---

## Architecture Flow

User Traffic
     ↓
FastAPI Application (Kubernetes Pod)
     ↓
Prometheus collects metrics
     ↓
AI Anomaly Detection Service
     ↓
ai_cpu_anomaly_score metric
     ↓
Grafana Dashboard
     ↓
Auto Remediation Script
     ↓
Kubernetes Self-Healing

---

## Features

- Kubernetes-based microservice deployment
- Real-time monitoring with Prometheus
- Grafana dashboards for observability
- AI anomaly detection for CPU usage
- Custom Prometheus metric `ai_cpu_anomaly_score`
- Automated remediation using Kubernetes restart
- Self-healing infrastructure
