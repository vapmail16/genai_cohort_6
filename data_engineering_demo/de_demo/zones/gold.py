from __future__ import annotations

import pandas as pd


def silver_to_gold(silver_df: pd.DataFrame) -> pd.DataFrame:
    g = silver_df.groupby("sku", as_index=False).agg(
        order_lines=("order_ref", "count"),
        total_qty=("qty", "sum"),
        total_amount=("amount", "sum"),
        first_seen=("txn_date", "min"),
        last_seen=("txn_date", "max"),
    )
    g["_gold_processed_at"] = pd.Timestamp.now(tz="UTC")
    return g.sort_values("sku").reset_index(drop=True)


def write_parquet(df: pd.DataFrame, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
