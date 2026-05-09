import pandas as pd

from de_demo.dq import checks


def test_completeness_flags_nulls():
    df = pd.DataFrame({"order_ref": ["a", None], "sku": ["s", "s2"]})
    r = checks.completeness_report(df, required_cols=["order_ref", "sku"])
    assert r["order_ref"]["null_count"] >= 1
    assert 0 <= r["_overall"]["completeness_ratio"] <= 1


def test_uniqueness_on_key():
    df = pd.DataFrame({"order_ref": ["a", "a", "b"]})
    r = checks.uniqueness_report(df, key_cols=["order_ref"])
    assert r["is_unique"] is False


def test_deduplication_counts():
    df = pd.DataFrame({"k": [1, 1, 2]})
    r = checks.deduplication_report(df, subset=["k"])
    assert r["duplicate_logical_rows"] >= 1


def test_business_rule_amount_matches_line():
    df = pd.DataFrame(
        {
            "qty": [2, 3],
            "unit_price": [10.0, 10.0],
            "amount": [20.0, 31.0],  # second row violates (off by > 0.02)
        }
    )
    r = checks.business_rule_amount_equals_qty_times_price(df, tolerance=0.02)
    assert r["passed"] is False
    assert r["violation_row_count"] >= 1


def test_run_all_dq_returns_summary():
    df = pd.DataFrame(
        {
            "order_ref": ["a", "b"],
            "sku": ["x", "y"],
            "qty": [1, 2],
            "unit_price": [10.0, 5.0],
            "amount": [10.0, 10.0],
        }
    )
    s = checks.run_all(df, key_cols=["order_ref"])
    assert "completeness" in s
    assert "uniqueness" in s
    assert "deduplication" in s
    assert "business_rule_line_total" in s
