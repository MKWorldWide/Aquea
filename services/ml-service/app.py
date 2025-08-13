
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Aquea ML Service", version="0.1.0")

class Sensors(BaseModel):
    ph: float | None = None
    tds_ppm: float | None = None
    turbidity_ntu: float | None = None
    temp_c: float | None = None
    flow_lpm: float | None = None
    pressure_kpa: float | None = None

class PredictRequest(BaseModel):
    sensors: Sensors

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/predict")
def predict(req: PredictRequest):
    vals = [v for v in [
        req.sensors.ph, req.sensors.tds_ppm, req.sensors.turbidity_ntu,
        req.sensors.temp_c, req.sensors.flow_lpm, req.sensors.pressure_kpa
    ] if v is not None]
    if not vals:
        return {"anomaly_score": 0.0, "is_anomaly": False}
    arr = np.array(vals, dtype=float)
    score = float(np.mean(np.abs(arr - np.mean(arr)) / (np.std(arr) + 1e-6)))
    return {"anomaly_score": score, "is_anomaly": bool(score > 2.5)}
