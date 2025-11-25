# app_api/main.py
from datetime import date
from typing import List, Optional

from fastapi import FastAPI, Depends, Query
from sqlalchemy import text
from sqlalchemy.engine import Connection

from .db import get_db
from .models import (
    SummaryMetrics,
    OnTimeByDay,
    RoutePerformance,
    DriverPerformance,
)

app = FastAPI(
    title="Supply Chain Delivery Performance API",
    version="0.1.0",
    description="API exposing delivery performance metrics from the supply_chain database.",
)


@app.get("/health", tags=["health"])
def health_check(conn: Connection = Depends(get_db)):
    result = conn.execute(text("SELECT 1")).scalar_one()
    return {"status": "ok", "db": result}


@app.get("/metrics/summary", response_model=SummaryMetrics, tags=["metrics"])
def get_summary_metrics(conn: Connection = Depends(get_db)):
    query = text(
        """
        SELECT
            COUNT(*) AS total_shipments,
            ROUND(AVG(CASE WHEN on_time THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct,
            ROUND(AVG(transit_hours), 2) AS avg_transit_hours
        FROM shipment_delivery_summary;
        """
    )
    row = conn.execute(query).mappings().one()
    return SummaryMetrics(
        total_shipments=row["total_shipments"],
        on_time_rate_pct=float(row["on_time_rate_pct"] or 0),
        avg_transit_hours=float(row["avg_transit_hours"] or 0),
    )


@app.get(
    "/metrics/on_time_by_day",
    response_model=List[OnTimeByDay],
    tags=["metrics"],
)
def get_on_time_by_day(
    conn: Connection = Depends(get_db),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
):
    base_query = """
        SELECT
            DATE(created_at) AS ship_date,
            COUNT(*) AS total,
            ROUND(AVG(CASE WHEN on_time THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct
        FROM shipment_delivery_summary
    """

    conditions = []
    params = {}

    if start:
        conditions.append("created_at >= :start")
        params["start"] = start
    if end:
        conditions.append("created_at < :end")
        params["end"] = end

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    base_query += " GROUP BY DATE(created_at) ORDER BY ship_date;"

    rows = conn.execute(text(base_query), params).mappings().all()

    return [
        OnTimeByDay(
            ship_date=row["ship_date"],
            total=row["total"],
            on_time_rate_pct=float(row["on_time_rate_pct"] or 0),
        )
        for row in rows
    ]


@app.get(
    "/metrics/routes_worst",
    response_model=List[RoutePerformance],
    tags=["metrics"],
)
def get_worst_routes(
    conn: Connection = Depends(get_db),
    min_shipments: int = Query(10, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    query = text(
        """
        SELECT
            dest_state,
            ROUND(AVG(transit_hours), 2) AS avg_transit_hours,
            ROUND(AVG(CASE WHEN on_time THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct,
            COUNT(*) AS shipments
        FROM shipment_delivery_summary
        GROUP BY dest_state
        HAVING COUNT(*) >= :min_shipments
        ORDER BY avg_transit_hours DESC
        LIMIT :limit;
        """
    )

    rows = conn.execute(
        query,
        {"min_shipments": min_shipments, "limit": limit},
    ).mappings().all()

    return [
        RoutePerformance(
            dest_state=row["dest_state"],
            avg_transit_hours=float(row["avg_transit_hours"] or 0),
            on_time_rate_pct=float(row["on_time_rate_pct"] or 0),
            shipments=row["shipments"],
        )
        for row in rows
    ]


@app.get(
    "/drivers/leaderboard",
    response_model=List[DriverPerformance],
    tags=["drivers"],
)
def get_driver_leaderboard(
    conn: Connection = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
):
    query = text(
        """
        SELECT
            d.driver_id,
            d.name,
            d.region,
            COUNT(*) AS total_shipments,
            ROUND(AVG(CASE WHEN sds.on_time THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct,
            ROUND(AVG(sds.transit_hours), 2) AS avg_transit_hours
        FROM driver_assignments da
        JOIN drivers d ON da.driver_id = d.driver_id
        JOIN shipment_delivery_summary sds ON da.shipment_id = sds.shipment_id
        GROUP BY d.driver_id, d.name, d.region
        ORDER BY on_time_rate_pct DESC
        LIMIT :limit;
        """
    )

    rows = conn.execute(query, {"limit": limit}).mappings().all()

    return [
        DriverPerformance(
            driver_id=row["driver_id"],
            name=row["name"],
            region=row["region"],
            total_shipments=row["total_shipments"],
            on_time_rate_pct=float(row["on_time_rate_pct"] or 0),
            avg_transit_hours=float(row["avg_transit_hours"] or 0),
        )
        for row in rows
    ]
