# app_api/models.py
from datetime import date
from pydantic import BaseModel


class SummaryMetrics(BaseModel):
    total_shipments: int
    on_time_rate_pct: float
    avg_transit_hours: float


class OnTimeByDay(BaseModel):
    ship_date: date
    total: int
    on_time_rate_pct: float


class RoutePerformance(BaseModel):
    dest_state: str
    avg_transit_hours: float
    on_time_rate_pct: float
    shipments: int


class DriverPerformance(BaseModel):
    driver_id: str
    name: str
    region: str
    total_shipments: int
    on_time_rate_pct: float
    avg_transit_hours: float
