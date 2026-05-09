from pathlib import Path

import sqlalchemy as sa

from de_demo import config
from de_demo.ingest.sqlite_ingest import read_raw_orders
from de_demo.seed.sqlite_seed import seed_source_sqlite


def test_seed_produces_exactly_hundred_sqlite_rows(tmp_path):
    p = Path(tmp_path) / "s.db"
    seed_source_sqlite(sqlite_path=p, table_name="raw_orders", row_count=100)
    df = read_raw_orders(p, table_name="raw_orders")
    assert len(df) == 100


def test_read_sqlite_via_engine_matches_table_name(tmp_path):
    p = Path(tmp_path) / "s.db"
    seed_source_sqlite(sqlite_path=p, table_name=config.SOURCE_TABLE, row_count=100)
    eng = sa.create_engine(f"sqlite:///{p}")
    with eng.connect() as c:
        n = c.execute(sa.text(f"SELECT COUNT(*) FROM {config.SOURCE_TABLE}")).scalar_one()
    assert n == 100
