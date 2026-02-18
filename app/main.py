from fastapi import FastAPI
import random
import time
import os

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Prometheus metrics setup
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/")
def home():
    return {"message": "AIOps SRE Platform running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/error")
def error():
    if random.randint(1, 2) == 1:
        raise Exception("Simulated application crash error!")
    return {"message": "No error this time"}

@app.get("/cpu")
def cpu_load():
    start = time.time()
    while time.time() - start < 10:
        _ = random.random() * random.random()
    return {"message": "CPU load generated for 10 seconds"}

@app.get("/slow")
def slow():
    time.sleep(5)
    return {"message": "Slow response simulated"}

@app.get("/env")
def env():
    return {"hostname": os.getenv("HOSTNAME", "unknown")}
