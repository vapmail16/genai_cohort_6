"""
PostgreSQL / SQLite warehouse DDL for medallion load.

Source (SQLite) reference table: raw_orders(
  order_ref, sku, qty, unit_price, amount, txn_date, customer_email, customer_phone
)

Load targets: silver_orders (cleaned + PII masked), gold_sku_summary (aggregates).
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Connection

POSTGRES_DDL = """
CREATE TABLE IF NOT EXISTS silver_orders (
    order_ref TEXT NOT NULL,
    sku TEXT NOT NULL,
    qty NUMERIC NOT NULL,
    unit_price NUMERIC NOT NULL,
    amount NUMERIC NOT NULL,
    txn_date TEXT NOT NULL,
    customer_email_masked TEXT,
    customer_phone_masked TEXT,
    pii_policy TEXT NOT NULL,
    _silver_processed_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT silver_orders_pkey PRIMARY KEY (order_ref)
);

CREATE TABLE IF NOT EXISTS gold_sku_summary (
    sku TEXT NOT NULL,
    order_lines BIGINT NOT NULL,
    total_qty NUMERIC NOT NULL,
    total_amount NUMERIC NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    _gold_processed_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT gold_sku_summary_pkey PRIMARY KEY (sku)
);
"""

SQLITE_DDL = """
CREATE TABLE IF NOT EXISTS silver_orders (
    order_ref TEXT NOT NULL,
    sku TEXT NOT NULL,
    qty REAL NOT NULL,
    unit_price REAL NOT NULL,
    amount REAL NOT NULL,
    txn_date TEXT NOT NULL,
    customer_email_masked TEXT,
    customer_phone_masked TEXT,
    pii_policy TEXT NOT NULL,
    _silver_processed_at TEXT NOT NULL,
    PRIMARY KEY (order_ref)
);

CREATE TABLE IF NOT EXISTS gold_sku_summary (
    sku TEXT NOT NULL,
    order_lines INTEGER NOT NULL,
    total_qty REAL NOT NULL,
    total_amount REAL NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    _gold_processed_at TEXT NOT NULL,
    PRIMARY KEY (sku)
);
"""


def _split_ddl(script: str) -> list[str]:
    return [s.strip() for s in script.split(";") if s.strip()]


def ensure_warehouse_tables(connection: Connection) -> None:
    name = connection.engine.dialect.name
    ddl = POSTGRES_DDL if name == "postgresql" else SQLITE_DDL
    for stmt in _split_ddl(ddl):
        connection.execute(text(stmt))


def truncate_medallion_tables(connection: Connection) -> None:
    name = connection.engine.dialect.name
    if name == "postgresql":
        connection.execute(
            text("TRUNCATE TABLE silver_orders, gold_sku_summary RESTART IDENTITY")
        )
    else:
        connection.execute(text("DELETE FROM silver_orders"))
        connection.execute(text("DELETE FROM gold_sku_summary"))


def ensure_database_objects(database_url: str) -> None:
    """Idempotent DDL only (admin init or first-time Postgres setup outside the pipeline)."""
    from sqlalchemy import create_engine

    eng = create_engine(database_url)
    with eng.begin() as conn:
        ensure_warehouse_tables(conn)
