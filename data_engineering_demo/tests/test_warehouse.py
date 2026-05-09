import pandas as pd
import sqlalchemy as sa

from de_demo.warehouse import postgres_sink


def test_write_frames_respects_target_schema_sqlite(tmp_path):
    url = f"sqlite:///{tmp_path/'wh.db'}"
    ts = pd.Timestamp.now(tz="UTC")
    sil = pd.DataFrame(
        {
            "order_ref": ["O1"],
            "sku": ["S1"],
            "qty": [1.0],
            "unit_price": [10.0],
            "amount": [10.0],
            "txn_date": ["2026-01-01"],
            "customer_email_masked": ["ab***@x.com"],
            "customer_phone_masked": ["***1234"],
            "pii_policy": ["contact_fields_redacted_in_silver"],
            "_silver_processed_at": [ts],
        }
    )
    gold = pd.DataFrame(
        {
            "sku": ["S1"],
            "order_lines": [1],
            "total_qty": [1.0],
            "total_amount": [10.0],
            "first_seen": ["2026-01-01"],
            "last_seen": ["2026-01-01"],
            "_gold_processed_at": [ts],
        }
    )
    postgres_sink.write_medallion_tables(url, silver_df=sil, gold_df=gold)
    eng = sa.create_engine(url)
    with eng.connect() as c:
        n = c.execute(sa.text("SELECT COUNT(*) FROM silver_orders")).scalar_one()
        assert n == 1
        cols = {r[1] for r in c.execute(sa.text("PRAGMA table_info(silver_orders)")).all()}
    assert "customer_email_masked" in cols
    assert "pii_policy" in cols
