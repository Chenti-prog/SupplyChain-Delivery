# app_api/db.py
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection


DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://localhost:5432/supply_chain"
    # or e.g.: "postgresql+psycopg2://postgres:postgres@localhost:5432/supply_chain"
)

engine = create_engine(DB_URL, future=True)


def get_db() -> Generator[Connection, None, None]:
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
