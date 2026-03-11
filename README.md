# AI-Driven AIOps SRE Platform

## Tech Stack
- Kubernetes
- Prometheus
- Grafana
- FastAPI
- Python
- Machine Learning

## Architecture

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
