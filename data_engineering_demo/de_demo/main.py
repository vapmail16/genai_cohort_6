from __future__ import annotations

import argparse
import json
import sys

from sqlalchemy.exc import OperationalError

from de_demo import config
from de_demo.pipeline.orchestrator import run_pipeline
from de_demo.warehouse.schema import ensure_database_objects


def bootstrap_instructions_text() -> str:
    sql_path = (config.PACKAGE_ROOT / "postgres" / "bootstrap_local_roles.sql").resolve()
    lines = [
        "Local PostgreSQL setup (no Docker):",
        "",
        "1) Start the server (examples: `brew services start postgresql@16`, or open Postgres.app).",
        "   Check: `pg_isready -h 127.0.0.1 -p 5432`",
        "",
        "2) As a superuser (often `-U postgres`; on Mac your login user may work), run:",
        f"   psql -h 127.0.0.1 -p 5432 -U postgres -f {sql_path}",
        "",
        "3) Create warehouse tables once (optional; pipeline also applies DDL):",
        "   python -m de_demo --init-warehouse-only",
        "",
        "4) Run the pipeline:",
        "   python -m de_demo --rows 100",
        "",
        "Docker Compose Postgres instead: export WAREHOUSE_HOST_PORT=5433",
        "Full URL override: export DATABASE_URL=postgresql+psycopg2://…",
        "Skip warehouse load entirely: python -m de_demo --skip-warehouse",
        "",
    ]
    return "\n".join(lines)


def _warehouse_connect_help() -> None:
    url = config.warehouse_url()
    sql_path = (config.PACKAGE_ROOT / "postgres" / "bootstrap_local_roles.sql").resolve()
    msg = (
        "\nPostgreSQL is not reachable at:\n"
        f"  {url}\n\n"
        "- Start Postgres and ensure port 5432 accepts TCP (try: pg_isready -h 127.0.0.1 -p 5432).\n"
        "- Create role/database once with:\n"
        f"  psql … -f {sql_path}\n\n"
        "Print full steps:\n"
        "  python -m de_demo --bootstrap-instructions\n\n"
        "Compose mapping 5433→5432:\n"
        "  export WAREHOUSE_HOST_PORT=5433\n\n"
        "Without warehouse:\n"
        "  python -m de_demo --skip-warehouse\n\n"
    )
    print(msg, file=sys.stderr)


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Run SQLite → medallion → PostgreSQL demo pipeline.")
    parser.add_argument("--rows", type=int, default=100, help="SQLite source row count (capped fixture).")
    parser.add_argument(
        "--bootstrap-instructions",
        action="store_true",
        help="Print local Postgres setup steps (paths and psql example), then exit.",
    )
    parser.add_argument(
        "--skip-warehouse",
        action="store_true",
        help="Complete pipeline without failing when Postgres is unreachable (SQLite + layers + reports only).",
    )
    parser.add_argument(
        "--init-warehouse-only",
        action="store_true",
        help="Create warehouse tables (silver_orders, gold_sku_summary) if missing, then exit.",
    )
    args = parser.parse_args()
    if args.bootstrap_instructions:
        print(bootstrap_instructions_text(), end="")
        return
    if args.init_warehouse_only:
        try:
            ensure_database_objects(config.warehouse_url())
        except OperationalError:
            _warehouse_connect_help()
            raise SystemExit(1) from None
        print(json.dumps({"warehouse_init": "ok", "database_url": config.warehouse_url()}))
        return
    try:
        out = run_pipeline(
            row_count=args.rows,
            skip_warehouse_if_unreachable=args.skip_warehouse,
        )
    except OperationalError:
        _warehouse_connect_help()
        raise SystemExit(1) from None
    print(json.dumps({k: v for k, v in out.items() if k != "dq_silver"}, indent=2, default=str))


if __name__ == "__main__":
    run_cli()
