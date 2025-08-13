
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations
import os, json
import psycopg
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

DB_DSN = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = "aquea/site/+/device/+/measurement"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT with code:", reason_code)
    client.subscribe(TOPIC, qos=1)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
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
                        "record_hash": payload.get("record_hash", ""),
                    },
                )
        print("Inserted from MQTT:", payload.get("site_id"), payload.get("device_id"))
    except Exception as e:
        print("Error processing message:", e)

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_forever()
