"""One-shot medallion orchestration."""

from __future__ import annotations

import json
from pathlib import Path

from de_demo import config
from de_demo.dq import checks
from de_demo.ingest.sqlite_ingest import read_raw_orders
from de_demo.reports import builder
from de_demo.seed.sqlite_seed import seed_source_sqlite
from de_demo.warehouse import postgres_sink
from de_demo.zones import bronze, gold, silver


def run_pipeline(
    *,
    warehouse_url: str | None = None,
    row_count: int = 100,
    skip_warehouse_if_unreachable: bool = False,
) -> dict:
    config.ensure_data_dirs()
    sqlite_path = config.SOURCE_SQLITE_PATH
    seed_source_sqlite(
        sqlite_path=sqlite_path, table_name=config.SOURCE_TABLE, row_count=row_count
    )

    raw = read_raw_orders(sqlite_path, table_name=config.SOURCE_TABLE)
    dq_bronze = checks.run_all(raw, key_cols=["order_ref"])
    dq_bronze_path = Path(config.DATA_ROOT) / "reports" / "dq_bronze.json"
    dq_bronze_path.parent.mkdir(parents=True, exist_ok=True)
    dq_bronze_path.write_text(json.dumps(dq_bronze, indent=2, default=str))

    bronze_df = bronze.land_snapshot(raw)
    bronze_parquet = config.BRONZE_DIR / "orders.parquet"
    bronze.write_parquet(bronze_df, bronze_parquet)

    silver_df, silver_meta = silver.bronze_to_silver(
        bronze_df, business_keys=["order_ref"]
    )
    dq_silver = checks.run_all(silver_df, key_cols=["order_ref"])
    silver_parquet = config.SILVER_DIR / "orders.parquet"
    silver.write_parquet(silver_df, silver_parquet)

    gold_df = gold.silver_to_gold(silver_df)
    dq_gold_note = checks.completeness_report(
        gold_df,
        required_cols=[
            c
            for c in ("sku", "order_lines", "total_qty", "total_amount")
            if c in gold_df.columns
        ],
    )
    gold_parquet = config.GOLD_DIR / "sku_summary.parquet"
    gold.write_parquet(gold_df, gold_parquet)

    url = warehouse_url or config.warehouse_url()
    warehouse_status = "skipped"
    try:
        postgres_sink.write_medallion_tables(
            url, silver_df=silver_df, gold_df=gold_df
        )
        warehouse_status = "loaded"
    except Exception as exc:
        warehouse_status = f"failed: {exc}"
        if not skip_warehouse_if_unreachable:
            raise

    report_path = Path(config.DATA_ROOT) / "reports" / "pipeline_summary.txt"
    outline = builder.build_live_summary(
        row_counts={
            "source_sqlite_raw": len(raw),
            "bronze": len(bronze_df),
            "silver": len(silver_df),
            "gold_skus": len(gold_df),
        },
        silver_meta=silver_meta,
        dq_silver=dq_silver,
        dq_bronze_highlights={
            "uniqueness": dq_bronze["uniqueness"],
            "line_rule": dq_bronze["business_rule_line_total"],
        },
        warehouse_status=warehouse_status,
        warehouse_url=url,
        paths={
            "sqlite_source": sqlite_path,
            "bronze_parquet": bronze_parquet,
            "silver_parquet": silver_parquet,
            "gold_parquet": gold_parquet,
        },
    )
    builder.write_report(report_path, outline)

    return {
        "row_counts": {
            "raw": len(raw),
            "bronze": len(bronze_df),
            "silver": len(silver_df),
            "gold": len(gold_df),
        },
        "silver_meta": silver_meta,
        "dq_silver": dq_silver,
        "warehouse_status": warehouse_status,
        "report_file": str(report_path),
        "dq_bronze_file": str(dq_bronze_path),
        "dq_gold_completeness": dq_gold_note,
    }
