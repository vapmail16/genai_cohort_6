import pandas as pd

from de_demo.zones import bronze, gold, silver


def sample_raw():
    # includes duplicate business key order_ref across two rows → silver keeps one
    return pd.DataFrame(
        {
            "order_ref": ["O1", "O1", "O2"],
            "sku": ["S1", "S1", "S2"],
            "qty": [1, 1, -1],
            "unit_price": [10.0, 10.0, 5.0],
            "amount": [10.0, 10.0, -5.0],
            "txn_date": ["2026-01-01", "2026-01-01", "2026-01-02"],
            "customer_email": ["a@x.com", "a@x.com", "b@x.com"],
            "customer_phone": ["1112223333", "1112223333", "4445556666"],
        }
    )


def test_silver_cleans_dtypes_dedups_and_positive_qty_filter():
    raw = sample_raw()
    out, meta = silver.bronze_to_silver(raw, business_keys=["order_ref"])
    assert meta["duplicate_rows_removed"] >= 1
    assert meta["silver_row_count_after_dedupe"] <= 2
    # negative qty dropped in cleaning rule
    assert (out["qty"] > 0).all()
    assert out["order_ref"].is_unique


def test_gold_aggregates_by_sku():
    sil = pd.DataFrame(
        {
            "order_ref": ["A", "B", "C"],
            "sku": ["S1", "S1", "S2"],
            "qty": [2, 3, 1],
            "unit_price": [10.0, 10.0, 50.0],
            "amount": [20.0, 30.0, 50.0],
            "txn_date": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "customer_email_masked": ["a***", "b***", "c***"],
        }
    )
    g = gold.silver_to_gold(sil)
    s1 = g[g["sku"] == "S1"].iloc[0]
    assert s1["order_lines"] == 2
    assert s1["total_qty"] == 5


def test_bronze_passthrough_adds_land_ts():
    raw = pd.DataFrame({"order_ref": ["O1"], "qty": [1]})
    b = bronze.land_snapshot(raw)
    assert "_bronze_ingested_at" in b.columns
