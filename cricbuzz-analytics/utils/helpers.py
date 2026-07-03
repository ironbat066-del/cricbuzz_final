"""Shared Streamlit / database helpers."""

from __future__ import annotations

import pandas as pd

from database.connection import get_connection


def read_sql(query: str, params: tuple | None = None) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql(query, conn, params=params)
    finally:
        conn.close()


def execute_sql(query: str, params: tuple | None = None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()


def db_counts() -> dict[str, int]:
    conn = get_connection()
    cur = conn.cursor()
    counts = {}
    for table in ("matches", "players", "venue_country_map", "player_format_stats"):
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cur.fetchone()[0]
    cur.close()
    conn.close()
    return counts
