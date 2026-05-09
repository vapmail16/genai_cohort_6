from __future__ import annotations

import pandas as pd

from de_demo.governance import pii


def bronze_to_silver(
    bronze_df: pd.DataFrame,
    *,
    business_keys: list[str],
) -> tuple[pd.DataFrame, dict]:
    df = bronze_df.copy()
    meta: dict[str, object] = {"silver_input_rows": len(df)}
    df = df.drop(columns=[c for c in ("_bronze_ingested_at",) if c in df.columns], errors="ignore")
    df = pii.redact_contact_columns(df)
    df = pii.tag_pii_policy(df)

    df = df.rename(
        columns={
            "customer_email": "customer_email_masked",
            "customer_phone": "customer_phone_masked",
        }
    )

    df = df.assign(_silver_processed_at=pd.Timestamp.now(tz="UTC"))
    df = df[df["qty"].notna() & (df["qty"] > 0)]

    variance = (
        df["amount"].astype(float)
        - df["qty"].astype(float) * df["unit_price"].astype(float)
    ).abs()
    line_ok = variance <= 0.02
    meta["line_total_rejects"] = int((~line_ok).sum())
    df = df[line_ok]

    before_dedupe = len(df)
    subset = business_keys if business_keys else None
    out = df.drop_duplicates(subset=subset, keep="last").reset_index(drop=True)
    meta.update(
        {
            "silver_rows_before_dedupe": before_dedupe,
            "duplicate_rows_removed": before_dedupe - len(out),
            "silver_row_count_after_dedupe": len(out),
        }
    )
    return out, meta


def write_parquet(df: pd.DataFrame, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
