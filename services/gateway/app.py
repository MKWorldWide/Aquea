
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations
import os, json, pathlib, datetime as dt
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from ledger import Ledger

load_dotenv()
DB_DSN = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
LEDGER_PATH = os.getenv("LEDGER_PATH", "/app/data/ledger.jsonl")

app = FastAPI(title="Aquea Gateway", version="0.1.0")
ledger = Ledger(pathlib.Path(LEDGER_PATH))

class Sensors(BaseModel):
    ph: float | None = None
    tds_ppm: float | None = None
    turbidity_ntu: float | None = None
    temp_c: float | None = None
    flow_lpm: float | None = None
    pressure_kpa: float | None = None

class Measurement(BaseModel):
    ts: dt.datetime = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc))
    site_id: str
    device_id: str
    sensors: Sensors
    meta: dict = Field(default_factory=dict)

@app.get("/health")
def health():
    return {"ok": True, "ledger_entries": ledger.count()}

@app.post("/ingest")
def ingest(meas: Measurement):
    payload = json.loads(meas.model_dump_json())
    rec_hash = ledger.append(payload)
    try:
        with psycopg.connect(DB_DSN, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO measurements (ts, site_id, device_id, ph, tds_ppm, turbidity_ntu, temp_c, flow_lpm, pressure_kpa, meta, record_hash)
                    VALUES (%(ts)s, %(site_id)s, %(device_id)s, %(ph)s, %(tds_ppm)s, %(turbidity_ntu)s, %(temp_c)s, %(flow_lpm)s, %(pressure_kpa)s, %(meta)s, %(record_hash)s)
                    """,
                    {
                        "ts": payload["ts"],
                        "site_id": payload["site_id"],
                        "device_id": payload["device_id"],
                        "ph": payload["sensors"].get("ph"),
                        "tds_ppm": payload["sensors"].get("tds_ppm"),
                        "turbidity_ntu": payload["sensors"].get("turbidity_ntu"),
                        "temp_c": payload["sensors"].get("temp_c"),
                        "flow_lpm": payload["sensors"].get("flow_lpm"),
                        "pressure_kpa": payload["sensors"].get("pressure_kpa"),
                        "meta": json.dumps(payload.get("meta", {})),
                        "record_hash": rec_hash,
                    },
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"ok": True, "record_hash": rec_hash}

@app.get("/latest/{site_id}/{device_id}")
def latest(site_id: str, device_id: str):
    try:
        with psycopg.connect(DB_DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT ts, ph, tds_ppm, turbidity_ntu, temp_c, flow_lpm, pressure_kpa, meta, record_hash
                    FROM measurements
                    WHERE site_id = %s AND device_id = %s
                    ORDER BY ts DESC
                    LIMIT 1
                    """, (site_id, device_id)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="No data")
                return {
                    "ts": row[0].isoformat(),
                    "sensors": {
                        "ph": row[1],
                        "tds_ppm": row[2],
                        "turbidity_ntu": row[3],
                        "temp_c": row[4],
                        "flow_lpm": row[5],
                        "pressure_kpa": row[6],
                    },
                    "meta": row[7],
                    "record_hash": row[8],
                }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
