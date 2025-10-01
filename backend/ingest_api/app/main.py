from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os, json, time, httpx, pathlib

S3_PATH = os.environ.get("S3_PATH","/data/raw")
DDB_PATH = os.environ.get("DDB_PATH","/data/ddb.json")
FEATURE_URL = os.environ.get("FEATURE_URL","http://predict-api:8083/score")

app = FastAPI(title="Ingest API", version="0.1.0")

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

@app.post("/ingest")
async def ingest(data: Telemetry):
    # Persist raw to "S3" (local folder)
    pathlib.Path(S3_PATH).mkdir(parents=True, exist_ok=True)
    fname = f"{data.device_id}_{data.ts}.json"
    with open(os.path.join(S3_PATH, fname),"w") as f:
        json.dump(data.model_dump(), f)

    # Append to local "DynamoDB"
    _append_ddb(data.model_dump())

    # Call prediction score
    async with httpx.AsyncClient(timeout=3.0) as client:
        r = await client.post(FEATURE_URL, json=data.model_dump())
        scores = r.json()
    return {"stored": True, "scores": scores}

def _append_ddb(item):
    db = []
    os.makedirs(os.path.dirname(DDB_PATH), exist_ok=True)
    if os.path.exists(DDB_PATH):
        try:
            db = json.load(open(DDB_PATH,"r"))
        except Exception:
            db = []
    db.append(item)
    json.dump(db, open(DDB_PATH,"w"), indent=2)
