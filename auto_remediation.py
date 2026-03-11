import requests
import time
import os

PROM_URL = "http://localhost:9090/api/v1/query"
QUERY = "ai_cpu_anomaly_score"

while True:
    try:
        response = requests.get(PROM_URL, params={"query": QUERY})
        data = response.json()

        value = float(data["data"]["result"][0]["value"][1])

        print("AI anomaly value:", value)

        if value == 1:
            print("⚠️ Anomaly detected! Restarting FastAPI deployment...")

            os.system("kubectl rollout restart deployment aiops-fastapi -n aiops")

    except Exception as e:
        print("Error:", e)

    time.sleep(30)