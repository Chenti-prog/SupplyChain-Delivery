import uuid
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker()


def generate_shipments(n=500, start_date="2025-01-01", end_date="2025-01-31"):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    delta_days = (end - start).days

    service_levels = ["Same-Day", "Two-Day", "Standard"]
    carriers = ["Amazon Logistics", "UPS", "FedEx"]

    rows = []
    for _ in range(n):
        created_at = start + timedelta(days=random.randint(0, delta_days))
        shipment_id = str(uuid.uuid4())

        origin_city, origin_state = fake.city(), fake.state_abbr()
        dest_city, dest_state = fake.city(), fake.state_abbr()

        row = {
            "shipment_id": shipment_id,
            "order_id": fake.bothify(text="ORD#####"),
            "customer_id": fake.bothify(text="CUST####"),
            "origin_city": origin_city,
            "origin_state": origin_state,
            "dest_city": dest_city,
            "dest_state": dest_state,
            "carrier": random.choice(carriers),
            "service_level": random.choice(service_levels),
            "created_at": created_at,
        }
        rows.append(row)

    return pd.DataFrame(rows)


def generate_delivery_events(shipments_df: pd.DataFrame):
    events_rows = []
    for _, row in shipments_df.iterrows():
        shipment_id = row["shipment_id"]
        created_at = row["created_at"]

        # shipment moves from created -> out_for_delivery -> delivered
        out_for_delivery = created_at + timedelta(hours=random.randint(6, 48))

        # 20% late shipments
        is_late = random.random() < 0.2

        delay_hours = random.randint(1, 48) if is_late else random.randint(-4, 4)
        delivered_at = out_for_delivery + timedelta(hours=delay_hours)

        # CREATED
        events_rows.append({
            "shipment_id": shipment_id,
            "event_type": "CREATED",
            "event_timestamp": created_at,
            "location_city": row["origin_city"],
            "location_state": row["origin_state"],
            "reason": "",
        })

        # OUT_FOR_DELIVERY
        events_rows.append({
            "shipment_id": shipment_id,
            "event_type": "OUT_FOR_DELIVERY",
            "event_timestamp": out_for_delivery,
            "location_city": row["dest_city"],
            "location_state": row["dest_state"],
            "reason": "",
        })

        # Optional DELAYED
        if is_late:
            events_rows.append({
                "shipment_id": shipment_id,
                "event_type": "DELAYED",
                "event_timestamp": out_for_delivery + timedelta(hours=2),
                "location_city": row["dest_city"],
                "location_state": row["dest_state"],
                "reason": random.choice([
                    "Weather",
                    "Traffic",
                    "Address issue",
                    "Mechanical problem",
                ]),
            })

        # DELIVERED
        events_rows.append({
            "shipment_id": shipment_id,
            "event_type": "DELIVERED",
            "event_timestamp": delivered_at,
            "location_city": row["dest_city"],
            "location_state": row["dest_state"],
            "reason": "",
        })

    return pd.DataFrame(events_rows)


if __name__ == "__main__":
    shipments = generate_shipments(n=500)
    events = generate_delivery_events(shipments)

    data_dir = "data/raw_data"
    shipments.to_csv(f"{data_dir}/shipments.csv", index=False)
    events.to_csv(f"{data_dir}/delivery_events.csv", index=False)

    print("✅ Generated data/raw/shipments.csv and data/raw/delivery_events.csv")
