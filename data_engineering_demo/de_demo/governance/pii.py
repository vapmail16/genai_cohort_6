from __future__ import annotations

import pandas as pd


def mask_email(val: object) -> object:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return val
    s = str(val).strip()
    if not s:
        return val
    if "@" not in s:
        return "***"
    local, _, domain = s.partition("@")
    if not local:
        return f"***@{domain}"
    hint = local[:2] if len(local) >= 2 else "*"
    return f"{hint}***@{domain}"


def mask_phone(val: object) -> object:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return val
    s = str(val).strip()
    if len(s) < 4:
        return "***"
    return f"***{s[-4:]}"


def redact_contact_columns(
    df: pd.DataFrame,
    *,
    email_col: str = "customer_email",
    phone_col: str = "customer_phone",
) -> pd.DataFrame:
    out = df.copy()
    if email_col in out.columns:
        out[email_col] = out[email_col].map(mask_email)
    if phone_col in out.columns:
        out[phone_col] = out[phone_col].map(mask_phone)
    return out


def tag_pii_policy(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["pii_policy"] = "contact_fields_redacted_in_silver"
    return out
