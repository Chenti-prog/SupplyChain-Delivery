-- New tables for drivers and their assignments

CREATE TABLE IF NOT EXISTS drivers (
    driver_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    region      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS driver_assignments (
    id          SERIAL PRIMARY KEY,
    shipment_id TEXT NOT NULL REFERENCES shipments (shipment_id) ON DELETE CASCADE,
    driver_id   TEXT NOT NULL REFERENCES drivers (driver_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_driver_assignments_driver_id
    ON driver_assignments (driver_id);

CREATE INDEX IF NOT EXISTS idx_driver_assignments_shipment_id
    ON driver_assignments (shipment_id);
