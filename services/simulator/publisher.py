
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations
import os, json, time, datetime as dt, random
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
SITE = "demo-site"
DEVICE = "esp32-sim-01"
TOPIC = f"aquea/site/{SITE}/device/{DEVICE}/measurement"

def randfloat(a, b):
    return round(random.uniform(a, b), 3)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_HOST, MQTT_PORT, 60)

while True:
    payload = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "site_id": SITE,
        "device_id": DEVICE,
        "sensors": {
            "ph": randfloat(6.8, 7.6),
            "tds_ppm": randfloat(150, 350),
            "turbidity_ntu": randfloat(0.5, 3.0),
            "temp_c": randfloat(18, 30),
            "flow_lpm": randfloat(1.0, 6.0),
            "pressure_kpa": randfloat(150, 300)
        },
        "meta": {"firmware": "sim-0.0.1"}
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published ->", TOPIC, payload)
    time.sleep(2)
