-- Core tables for Supply Chain Delivery Performance

-- Drop tables while developing so you can rerun this file
DROP TABLE IF EXISTS delivery_events;
DROP TABLE IF EXISTS shipments;

-- Shipments table
CREATE TABLE shipments (
    shipment_id     TEXT PRIMARY KEY,
    order_id        TEXT NOT NULL,
    customer_id     TEXT NOT NULL,
    origin_city     TEXT NOT NULL,
    origin_state    TEXT NOT NULL,
    dest_city       TEXT NOT NULL,
    dest_state      TEXT NOT NULL,
    carrier         TEXT NOT NULL,
    service_level   TEXT NOT NULL,
    created_at      TIMESTAMP NOT NULL
);

-- Delivery events table
CREATE TABLE delivery_events (
    event_id        SERIAL PRIMARY KEY,
    shipment_id     TEXT NOT NULL REFERENCES shipments (shipment_id) ON DELETE CASCADE,
    event_type      TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    location_city   TEXT,
    location_state  TEXT,
    reason          TEXT
);

-- Helpful indexes for queries later
CREATE INDEX idx_shipments_created_at ON shipments (created_at);
CREATE INDEX idx_delivery_events_shipment_id ON delivery_events (shipment_id);
CREATE INDEX idx_delivery_events_event_timestamp ON delivery_events (event_timestamp);
CREATE INDEX idx_delivery_events_event_type ON delivery_events (event_type);
