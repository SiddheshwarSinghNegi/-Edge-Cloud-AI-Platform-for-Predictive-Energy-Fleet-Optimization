from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
import os, json, time, random, math

DDB_PATH = os.environ.get("DDB_PATH","/data/ddb.json")

app = FastAPI(title="Predict API", version="0.1.0")

class Telemetry(BaseModel):
    device_id: str
    ts: int
    voltage: float
    current: float
    temp: float
    status: str

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/score")
def score(x: Telemetry):
    # Mock feature extraction & transformer inference latency
    import time, random
    time.sleep(random.uniform(0.003,0.015))
    anomaly = round(random.random(), 4)
    demand_kw = round((x.voltage * x.current)/1000.0, 3)
    days = max(1, int(30 - (x.temp-25) - anomaly*10))
    result = {
        "device_id": x.device_id,
        "ts": x.ts,
        "anomaly_score": anomaly,
        "demand_kw": demand_kw,
        "next_service_days": days
    }
    _append_pred(result)
    return result

@app.get("/predictions/latest")
def latest(n: int = 10):
    preds = _load_preds()
    return preds[-n:] if preds else []

def _append_pred(rec: Dict[str, Any]):
    path = "/data/predictions.json"
    os.makedirs("/data", exist_ok=True)
    data = []
    if os.path.exists(path):
        data = json.load(open(path))
    data.append(rec)
    json.dump(data, open(path,"w"), indent=2)

def _load_preds():
    path = "/data/predictions.json"
    if os.path.exists(path):
        return json.load(open(path))
    return []
