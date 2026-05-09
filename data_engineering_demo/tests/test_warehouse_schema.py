import sqlalchemy as sa

from de_demo.warehouse.schema import ensure_database_objects


def test_ensure_database_objects_creates_tables_sqlite(tmp_path):
    url = f"sqlite:///{tmp_path/'wh.db'}"
    ensure_database_objects(url)
    eng = sa.create_engine(url)
    with eng.connect() as c:
        tables = c.execute(
            sa.text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        ).all()
    names = {t[0] for t in tables}
    assert "silver_orders" in names
    assert "gold_sku_summary" in names
