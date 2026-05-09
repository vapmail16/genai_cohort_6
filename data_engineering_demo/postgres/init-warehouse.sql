-- warehouse target schema (PostgreSQL ≥ 15 / 16)
-- Aligns with SQLite source columns after silver/gold transforms in de_demo pipeline.
-- Applied automatically on first `docker compose up` via docker-entrypoint-initdb.d.

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
