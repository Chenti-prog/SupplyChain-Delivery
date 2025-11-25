import os

import pandas as pd
from sqlalchemy import create_engine, text


# 🧠 Adjust this if you use a different user/password
# Option 1: no password, local user owns DB:
#   postgresql+psycopg2:///<dbname>
# Option 2: with user/pass:
#   postgresql+psycopg2://user:password@host:port/dbname
DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://localhost:5432/supply_chain"
    # Example with credentials:
    # "postgresql+psycopg2://postgres:postgres@localhost:5432/supply_chain"
)


def load_shipments(engine, csv_path: str):
    print(f"📥 Loading shipments from {csv_path} ...")
    df = pd.read_csv(csv_path, parse_dates=["created_at"])

    expected_cols = [
        "shipment_id",
        "order_id",
        "customer_id",
        "origin_city",
        "origin_state",
        "dest_city",
        "dest_state",
        "carrier",
        "service_level",
        "created_at",
    ]

    missing = set(expected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in shipments CSV: {missing}")

    # Avoid duplicate primary keys just in case
    df = df.drop_duplicates(subset=["shipment_id"])

    df.to_sql("shipments", engine, if_exists="append", index=False)
    print(f"✅ Inserted {len(df)} rows into shipments.")


def load_delivery_events(engine, csv_path: str):
    print(f"📥 Loading delivery events from {csv_path} ...")
    df = pd.read_csv(csv_path, parse_dates=["event_timestamp"])

    expected_cols = [
        "shipment_id",
        "event_type",
        "event_timestamp",
        "location_city",
        "location_state",
        "reason",
    ]

    missing = set(expected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in delivery_events CSV: {missing}")

    # event_id is SERIAL in DB, so we don't include it
    df.to_sql("delivery_events", engine, if_exists="append", index=False)
    print(f"✅ Inserted {len(df)} rows into delivery_events.")


def main():
    shipments_csv = "data/raw_data/shipments.csv"
    events_csv = "data/raw_data/delivery_events.csv"

    if not os.path.exists(shipments_csv):
        raise FileNotFoundError(f"{shipments_csv} not found. Run generate_synthetic_data.py first.")
    if not os.path.exists(events_csv):
        raise FileNotFoundError(f"{events_csv} not found. Run generate_synthetic_data.py first.")

    print(f"🔗 Connecting to database: {DB_URL}")
    engine = create_engine(DB_URL)

    # Quick connection test
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ DB connection OK, test query returned:", list(result))

    load_shipments(engine, shipments_csv)
    load_delivery_events(engine, events_csv)

    print("🎉 All data loaded successfully.")


if __name__ == "__main__":
    main()
