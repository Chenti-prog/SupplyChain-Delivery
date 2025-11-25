-- View: one row per shipment with delivery outcome/metrics

CREATE OR REPLACE VIEW shipment_delivery_summary AS
WITH delivered AS (
    SELECT
        shipment_id,
        MAX(event_timestamp) FILTER (WHERE event_type = 'DELIVERED') AS delivered_at
    FROM delivery_events
    GROUP BY shipment_id
)
SELECT
    s.shipment_id,
    s.order_id,
    s.customer_id,
    s.origin_city,
    s.origin_state,
    s.dest_city,
    s.dest_state,
    s.carrier,
    s.service_level,
    s.created_at,
    d.delivered_at,
    EXTRACT(EPOCH FROM (d.delivered_at - s.created_at)) / 3600.0 AS transit_hours,
    CASE
        WHEN s.service_level = 'Same-Day'
             AND d.delivered_at <= s.created_at + INTERVAL '1 day'
            THEN TRUE
        WHEN s.service_level = 'Two-Day'
             AND d.delivered_at <= s.created_at + INTERVAL '2 days'
            THEN TRUE
        WHEN s.service_level = 'Standard'
             AND d.delivered_at <= s.created_at + INTERVAL '5 days'
            THEN TRUE
        ELSE FALSE
    END AS on_time
FROM shipments s
JOIN delivered d USING (shipment_id);
