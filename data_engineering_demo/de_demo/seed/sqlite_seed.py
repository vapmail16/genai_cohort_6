from __future__ import annotations

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def seed_source_sqlite(*, sqlite_path, table_name: str, row_count: int = 100) -> None:
    rng = np.random.default_rng(42)
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    refs = [f"O{i:04d}" for i in range(row_count)]

    sku_pool = [f"S{j % 24:03d}-item" for j in range(row_count)]
    qty = rng.integers(1, 6, size=row_count)
    unit = np.round(rng.uniform(8.0, 120.0, size=row_count), 2)

    emails = [f"user{i % 37}@example.test" for i in range(row_count)]
    phones = [f"555-{1000 + i:03d}-{2000 + i:04d}" for i in range(row_count)]

    for i in (90, 91, 92):
        if i < row_count:
            qty[i] = -1

    for dup_idx in range(95, min(100, row_count)):
        src = dup_idx - 95
        refs[dup_idx] = refs[src]
        sku_pool[dup_idx] = sku_pool[src]
        qty[dup_idx] = qty[src]
        unit[dup_idx] = unit[src]
        emails[dup_idx] = emails[src]
        phones[dup_idx] = phones[src]

    amt = qty.astype(float) * unit.astype(float).copy()
    for i in (93, 94):
        if i < row_count:
            amt[i] += 50.0
    amt = np.round(amt, 2)

    txn = pd.to_datetime(rng.choice(pd.date_range("2026-01-01", periods=31), size=row_count))

    df = pd.DataFrame(
        {
            "order_ref": refs,
            "sku": sku_pool,
            "qty": qty,
            "unit_price": unit,
            "amount": amt,
            "txn_date": txn.strftime("%Y-%m-%d"),
            "customer_email": emails,
            "customer_phone": phones,
        }
    )

    eng = create_engine(f"sqlite:///{sqlite_path}")
    df.to_sql(table_name, eng, if_exists="replace", index=False)
