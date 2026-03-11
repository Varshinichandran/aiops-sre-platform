from fastapi import FastAPI, Request
import requests
import numpy as np
from sklearn.ensemble import IsolationForest
from prometheus_client import Gauge, Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

# ---------------------------------------------------
# REQUEST COUNT METRIC
# ---------------------------------------------------
REQUEST_COUNT = Counter(
    "fastapi_request_count_total",
    "Total HTTP requests"
)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    REQUEST_COUNT.inc()
    response = await call_next(request)
    return response


# ---------------------------------------------------
# PROMETHEUS CONFIG
# ---------------------------------------------------
PROM_URL = "http://monitoring-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090"

# AI anomaly metric for Prometheus
anomaly_gauge = Gauge(
    "ai_cpu_anomaly_score",
    "AI detected CPU anomaly (1 = anomaly, 0 = normal)"
)

# Isolation Forest model
model = IsolationForest(contamination=0.1)

# Store CPU history over time
history = []


# ---------------------------------------------------
# FETCH CPU DATA FROM PROMETHEUS
# ---------------------------------------------------
def fetch_cpu_data():
    query = 'rate(container_cpu_usage_seconds_total{namespace="aiops",pod=~"aiops-fastapi.*"}[1m])'
    url = f"{PROM_URL}/api/v1/query"

    try:
        response = requests.get(url, params={"query": query}, timeout=5)
        data = response.json()
    except Exception:
        return np.array([]).reshape(-1, 1)

    values = []
    for result in data.get("data", {}).get("result", []):
        try:
            values.append(float(result["value"][1]))
        except:
            pass

    return np.array(values).reshape(-1, 1) if values else np.array([]).reshape(-1, 1)


# ---------------------------------------------------
# ANOMALY DETECTION ENDPOINT
# ---------------------------------------------------
@app.get("/detect")
def detect_anomaly():
    global history

    data = fetch_cpu_data()

    if data.size == 0:
        return {"status": "No data from Prometheus"}

    # Take average CPU across pods
    current_value = float(np.mean(data))

    # Add to history
    history.append([current_value])

    # Keep only last 50 samples
    if len(history) > 50:
        history.pop(0)

    # Need minimum baseline samples
    if len(history) < 10:
        return {
            "status": "Collecting baseline data...",
            "samples_collected": len(history)
        }

    # Train model on history
    model.fit(history)
    predictions = model.predict(history)

    # Check latest value
    latest_prediction = predictions[-1]
    anomaly = 1 if latest_prediction == -1 else 0

    anomaly_gauge.set(anomaly)

    return {
        "current_cpu": current_value,
        "anomaly_detected": anomaly,
        "samples_used": len(history)
    }


# ---------------------------------------------------
# PROMETHEUS METRICS ENDPOINT
# ---------------------------------------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.get("/")
def root():
    return {"message": "AIOps SRE Platform running"}

import threading
import time

def run_detection_loop():
    while True:
        try:
            detect_anomaly()
        except:
            pass
        time.sleep(30)

thread = threading.Thread(target=run_detection_loop)
thread.daemon = True
thread.start()

