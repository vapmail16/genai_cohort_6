"""Load raw rows from SQLite (source system of record)."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine


def read_raw_orders(sqlite_path, *, table_name: str) -> pd.DataFrame:
    uri = f"sqlite:///{sqlite_path}"
    return pd.read_sql_table(table_name, create_engine(uri))
