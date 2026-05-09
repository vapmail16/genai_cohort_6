from __future__ import annotations

import pandas as pd

from de_demo.warehouse import schema


def write_medallion_tables(
    database_url: str,
    *,
    silver_df: pd.DataFrame,
    gold_df: pd.DataFrame,
) -> None:
    from sqlalchemy import create_engine

    eng = create_engine(database_url)
    with eng.begin() as conn:
        schema.ensure_warehouse_tables(conn)
        schema.truncate_medallion_tables(conn)
        silver_df.to_sql("silver_orders", conn, if_exists="append", index=False)
        gold_df.to_sql("gold_sku_summary", conn, if_exists="append", index=False)
