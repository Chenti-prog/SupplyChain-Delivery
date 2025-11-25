import os
import random

from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker()

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://localhost:5432/supply_chain"
    # or: "postgresql+psycopg2://postgres:postgres@localhost:5432/supply_chain"
)


def create_drivers(engine, n_drivers=15):
    regions = ["North", "South", "East", "West", "Central"]

    drivers = []
    for i in range(n_drivers):
        driver_id = f"DRV{i+1:03d}"
        name = fake.name()
        region = random.choice(regions)
        drivers.append((driver_id, name, region))

    with engine.begin() as conn:
        # Clear existing to avoid duplicates during dev
        conn.execute(text("DELETE FROM driver_assignments"))
        conn.execute(text("DELETE FROM drivers"))

        conn.execute(
            text(
                """
                INSERT INTO drivers (driver_id, name, region)
                VALUES (:driver_id, :name, :region)
                """
            ),
            [
                {"driver_id": d[0], "name": d[1], "region": d[2]}
                for d in drivers
            ],
        )

    print(f"✅ Inserted {len(drivers)} drivers.")


def assign_drivers_to_shipments(engine):
    with engine.begin() as conn:
        # Get all drivers
        drivers = conn.execute(text("SELECT driver_id FROM drivers")).fetchall()
        if not drivers:
            raise RuntimeError("No drivers found. Run create_drivers() first.")
        driver_ids = [row[0] for row in drivers]

        # Get all shipments
        shipments = conn.execute(text("SELECT shipment_id FROM shipments")).fetchall()
        shipment_ids = [row[0] for row in shipments]
        print(f"Assigning drivers to {len(shipment_ids)} shipments...")

        # Clear old assignments
        conn.execute(text("DELETE FROM driver_assignments"))

        batch = [
            {"shipment_id": sid, "driver_id": random.choice(driver_ids)}
            for sid in shipment_ids
        ]

        conn.execute(
            text(
                """
                INSERT INTO driver_assignments (shipment_id, driver_id)
                VALUES (:shipment_id, :driver_id)
                """
            ),
            batch,
        )

    print("✅ Driver assignments created.")


def main():
    print(f"🔗 Connecting to DB: {DB_URL}")
    engine = create_engine(DB_URL)

    # Quick check
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM shipments"))
        print("Shipments in DB:", result.scalar())

    create_drivers(engine, n_drivers=15)
    assign_drivers_to_shipments(engine)
    print("🎉 Done creating drivers and assignments.")


if __name__ == "__main__":
    main()
