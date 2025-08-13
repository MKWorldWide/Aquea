
# Architecture

- Device layer: ESP32-based sensor nodes measure pH, TDS, turbidity, temperature, flow, and pressure; control pumps/valves.
- Transport: MQTT (Mosquitto).
- Ingestion: `device-hub` consumes MQTT and writes to Postgres; `gateway` offers REST ingestion and maintains an integrity ledger (hash chain).
- ML: `ml-service` exposes a simple API now; evolve to autoencoder/MPC.
- Observability: Add Grafana/Temporal in future milestones.
- Security: Per-device keys, authN via mTLS/JWT in v0.2.
