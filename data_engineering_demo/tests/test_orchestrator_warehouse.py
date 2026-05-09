from __future__ import annotations

from unittest.mock import patch

import pytest

from de_demo import config
from de_demo.pipeline.orchestrator import run_pipeline


def _patch_data_roots(tmp_path, monkeypatch):
    root = tmp_path / "pipeline_data"
    monkeypatch.setattr(config, "DATA_ROOT", root)
    monkeypatch.setattr(config, "SOURCE_SQLITE_PATH", root / "source" / "orders.db")
    monkeypatch.setattr(config, "BRONZE_DIR", root / "bronze")
    monkeypatch.setattr(config, "SILVER_DIR", root / "silver")
    monkeypatch.setattr(config, "GOLD_DIR", root / "gold")
    monkeypatch.setattr(config, "REPORTS_DIR", root / "reports")


def test_skipping_warehouse_marks_failure_without_raises(tmp_path, monkeypatch):
    _patch_data_roots(tmp_path, monkeypatch)
    err = Exception("connection refused")
    with patch(
        "de_demo.pipeline.orchestrator.postgres_sink.write_medallion_tables",
        side_effect=err,
    ):
        out = run_pipeline(row_count=100, skip_warehouse_if_unreachable=True)
    assert out["row_counts"]["raw"] == 100
    assert "failed" in str(out["warehouse_status"])
    assert "Hint" not in str(out["warehouse_status"])


def test_default_strict_raises_when_warehouse_fails(tmp_path, monkeypatch):
    _patch_data_roots(tmp_path, monkeypatch)
    with patch(
        "de_demo.pipeline.orchestrator.postgres_sink.write_medallion_tables",
        side_effect=Exception("boom"),
    ):
        with pytest.raises(Exception, match="boom"):
            run_pipeline(row_count=20)
