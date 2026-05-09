from __future__ import annotations

import json
from pathlib import Path


def build_live_summary(
    *,
    row_counts: dict,
    silver_meta: dict,
    dq_silver: dict,
    dq_bronze_highlights: dict,
    warehouse_status: str,
    warehouse_url: str,
    paths: dict,
) -> str:
    lines = [
        "=== Data engineering demo — medallion run ===",
        "",
        "Row counts:",
        *[f"  - {k}: {v}" for k, v in row_counts.items()],
        "",
        "Silver transform:",
        *[f"  - {k}: {v}" for k, v in silver_meta.items()],
        "",
        "DQ highlights (bronze — expect issues on raw ingest):",
        f"  {json.dumps(dq_bronze_highlights, indent=4, default=str)}",
        "",
        "DQ (silver — post governance + cleaning):",
        f"  uniqueness: {json.dumps(dq_silver['uniqueness'], default=str)}",
        f"  completeness overall: "
        f"{dq_silver['completeness'].get('_overall', {}).get('completeness_ratio')}",
        f"  line total rule ok: "
        f"{dq_silver['business_rule_line_total'].get('passed')}",
        "",
        "Paths:",
        *[f"  - {k}: {v}" for k, v in paths.items()],
        "",
        f"Warehouse target: {warehouse_url}",
        f"Warehouse load: {warehouse_status}",
        "",
        "Governance: emails/phones masked in silver; tagged via pii_policy column.",
        "",
        "=== Demo complete ===",
        "",
    ]
    return "\n".join(lines)


def write_report(destination: Path, body: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(body, encoding="utf-8")
    print(body)
