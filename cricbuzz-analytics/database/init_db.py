"""Create schema and load seed data."""

from __future__ import annotations

from pathlib import Path

import mysql.connector

from config import MYSQL_CONFIG


def run_sql_file(path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    bootstrap = {k: v for k, v in MYSQL_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**bootstrap)
    cur = conn.cursor()
    for statement in sql.split(";"):
        stmt = statement.strip()
        if stmt:
            cur.execute(stmt)
    conn.commit()
    cur.close()
    conn.close()


def init_db(seed: bool = True) -> None:
    root = Path(__file__).resolve().parent
    run_sql_file(root / "schema.sql")
    if seed:
        from database.seed import seed as load_seed

        load_seed()
    print("Database ready.")


if __name__ == "__main__":
    init_db()
