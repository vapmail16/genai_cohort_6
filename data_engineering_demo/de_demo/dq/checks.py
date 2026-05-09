from __future__ import annotations

import numpy as np
import pandas as pd


def completeness_report(df: pd.DataFrame, *, required_cols: list[str]) -> dict:
    per: dict[str, dict] = {}
    total = len(df)
    ratios = []
    for c in required_cols:
        if c not in df.columns:
            per[c] = {"null_count": total, "present_ratio": 0.0}
            ratios.append(0.0)
            continue
        nulls = df[c].isna().sum()
        present = total - int(nulls)
        ratio = present / total if total else 1.0
        per[c] = {"null_count": int(nulls), "present_ratio": float(ratio)}
        ratios.append(ratio)
    overall = float(np.mean(ratios)) if ratios else 1.0
    per["_overall"] = {"completeness_ratio": overall, "row_count": total}
    return per


def uniqueness_report(df: pd.DataFrame, *, key_cols: list[str]) -> dict:
    if not key_cols or not len(df):
        return {"is_unique": True, "duplicate_key_rows": 0}
    dup = df.duplicated(subset=key_cols, keep=False).sum()
    return {
        "is_unique": bool(dup == 0),
        "duplicate_key_rows": int(dup),
        "distinct_keys": int(df.drop_duplicates(subset=key_cols).shape[0]),
    }


def deduplication_report(df: pd.DataFrame, *, subset: list[str]) -> dict:
    if not subset:
        return {"duplicate_logical_rows": 0}
    dup_count = len(df) - df.drop_duplicates(subset=subset).shape[0]
    return {"duplicate_logical_rows": int(dup_count)}


def business_rule_amount_equals_qty_times_price(
    df: pd.DataFrame, *, tolerance: float = 0.02
) -> dict:
    need = {"qty", "unit_price", "amount"}
    if not need.issubset(df.columns):
        return {"passed": True, "note": "columns_missing", "violation_row_count": 0}
    expected = df["qty"].astype(float) * df["unit_price"].astype(float)
    delta = (df["amount"].astype(float) - expected).abs()
    bad = delta > tolerance
    return {
        "passed": bool(not bad.any()),
        "violation_row_count": int(bad.sum()),
        "max_abs_variance": float(delta.max()) if len(delta) else 0.0,
    }


def run_all(df: pd.DataFrame, *, key_cols: list[str]) -> dict:
    req = ["order_ref", "sku", "qty", "unit_price", "amount", "txn_date"]
    present_req = [c for c in req if c in df.columns]
    return {
        "completeness": completeness_report(df, required_cols=present_req or req),
        "uniqueness": uniqueness_report(df, key_cols=key_cols),
        "deduplication": deduplication_report(df, subset=key_cols),
        "business_rule_line_total": business_rule_amount_equals_qty_times_price(df),
    }
