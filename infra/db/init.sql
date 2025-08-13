
CREATE TABLE IF NOT EXISTS measurements (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL,
  site_id TEXT NOT NULL,
  device_id TEXT NOT NULL,
  ph DOUBLE PRECISION,
  tds_ppm DOUBLE PRECISION,
  turbidity_ntu DOUBLE PRECISION,
  temp_c DOUBLE PRECISION,
  flow_lpm DOUBLE PRECISION,
  pressure_kpa DOUBLE PRECISION,
  meta JSONB,
  record_hash TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_measurements_ts ON measurements (ts);
CREATE INDEX IF NOT EXISTS idx_measurements_site_device ON measurements (site_id, device_id);
