from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote_plus

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILENAME = "docker-compose.yml"
DATA_ROOT = PACKAGE_ROOT / "data"
SOURCE_SQLITE_PATH = DATA_ROOT / "source" / "orders.db"
BRONZE_DIR = DATA_ROOT / "bronze"
SILVER_DIR = DATA_ROOT / "silver"
GOLD_DIR = DATA_ROOT / "gold"
REPORTS_DIR = DATA_ROOT / "reports"

SOURCE_TABLE = "raw_orders"


DEFAULT_LOCAL_POSTGRES_PORT = 5432
WAREHOUSE_HOST_PORT_ENV = "WAREHOUSE_HOST_PORT"


def warehouse_connection_from_compose(
    *, compose_package_root: Path | None = None
) -> tuple[str, str, str, int]:
    """
    Reads `POSTGRES_*` and published `HOST:5432` mapping from docker-compose.yml.

    The published host port is informational (e.g. Docker maps 5433→5432).
    For client connections, see `warehouse_url()`: local Postgres defaults to
    port ``DEFAULT_LOCAL_POSTGRES_PORT`` unless `WAREHOUSE_HOST_PORT` or
    `DATABASE_URL` is set.
    """
    root = compose_package_root or PACKAGE_ROOT
    path = root / COMPOSE_FILENAME
    if not path.is_file():
        raise FileNotFoundError(
            f"{COMPOSE_FILENAME} not found at {path}; set DATABASE_URL or restore compose file."
        )
    txt = path.read_text(encoding="utf-8")

    um = re.search(r"^\s*POSTGRES_USER:\s*(.+?)\s*$", txt, re.MULTILINE)
    pm = re.search(r"^\s*POSTGRES_PASSWORD:\s*(.+?)\s*$", txt, re.MULTILINE)
    dm = re.search(r"^\s*POSTGRES_DB:\s*(.+?)\s*$", txt, re.MULTILINE)
    if not um or not pm or not dm:
        raise ValueError(f"Missing POSTGRES_USER / PASSWORD / DB in {path}")

    def _scalar(s: str) -> str:
        s = s.split("#")[0].strip().strip("\"'").strip("'")
        return s

    port_m = re.search(r'-\s*["\']?\s*(\d+)\s*:\s*5432\s*["\']?', txt)
    if not port_m:
        raise ValueError(
            f"No host port mapped to Postgres container port 5432 in {path} "
            '(expected `- "HOST:5432"` under warehouse ports)'
        )

    host_port = int(port_m.group(1))
    return _scalar(um.group(1)), _scalar(pm.group(1)), _scalar(dm.group(1)), host_port


def warehouse_url(*, compose_package_root: Path | None = None) -> str:
    if url := os.environ.get("DATABASE_URL"):
        return url
    user, password, db, _compose_publish = warehouse_connection_from_compose(
        compose_package_root=compose_package_root
    )
    hp_raw = os.environ.get(WAREHOUSE_HOST_PORT_ENV, "").strip()
    host_port = int(hp_raw) if hp_raw else DEFAULT_LOCAL_POSTGRES_PORT
    return (
        f"postgresql+psycopg2://{quote_plus(user)}:"
        f"{quote_plus(password)}@127.0.0.1:{host_port}/{quote_plus(db)}"
    )


def ensure_data_dirs() -> None:
    for p in (
        SOURCE_SQLITE_PATH.parent,
        BRONZE_DIR,
        SILVER_DIR,
        GOLD_DIR,
        REPORTS_DIR,
    ):
        p.mkdir(parents=True, exist_ok=True)
