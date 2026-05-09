from __future__ import annotations

import pandas as pd


def land_snapshot(raw: pd.DataFrame) -> pd.DataFrame:
    out = raw.copy()
    out["_bronze_ingested_at"] = pd.Timestamp.now(tz="UTC")
    return out


def write_parquet(df: pd.DataFrame, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
