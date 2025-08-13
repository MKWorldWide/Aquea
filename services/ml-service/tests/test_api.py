from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json().get("ok") is True


def test_predict_empty():
    resp = client.post("/predict", json={"sensors": {}})
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_anomaly"] is False


def test_predict_values():
    payload = {
        "sensors": {
            "ph": 7.2,
            "tds_ppm": 220.0,
            "turbidity_ntu": 1.0,
            "temp_c": 23.0,
            "flow_lpm": 3.0,
            "pressure_kpa": 200.0,
        }
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "anomaly_score" in body



