from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os, json

DDB_PATH = os.environ.get("DDB_PATH","/data/ddb.json")
DEVICES_PATH = "/data/devices.json"

app = FastAPI(title="Devices API", version="0.1.0")

class Device(BaseModel):
    device_id: str
    location: Optional[str] = None
    type: Optional[str] = "ev_charger"
    status: Optional[str] = "active"

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/devices", response_model=List[Device])
def list_devices():
    return _load_all()

@app.post("/devices", response_model=Device)
def register_device(d: Device):
    devices = _load_all()
    if any(x.device_id == d.device_id for x in devices):
        raise HTTPException(409, "device exists")
    devices.append(d)
    _save_all(devices)
    return d

@app.delete("/devices/{device_id}")
def delete_device(device_id: str):
    devices = [d for d in _load_all() if d.device_id != device_id]
    _save_all(devices)
    return {"deleted": device_id}

def _load_all() -> List[Device]:
    if os.path.exists(DEVICES_PATH):
        return [Device(**x) for x in json.load(open(DEVICES_PATH))]
    return []

def _save_all(devs: List[Device]):
    os.makedirs(os.path.dirname(DEVICES_PATH), exist_ok=True)
    json.dump([d.model_dump() for d in devs], open(DEVICES_PATH,"w"), indent=2)
