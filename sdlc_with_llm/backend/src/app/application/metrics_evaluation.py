"""Application use-case: evaluate in-memory fixture metrics."""

from __future__ import annotations

import json
from pathlib import Path

from app.domain.models import MetricEvaluation, MetricRecord
from app.domain.recommendation_engine import recommend_for_metric

_FIXTURE_PATH = Path(__file__).resolve().parents[3] / "data" / "sample_metrics.json"


def _load_records(path: Path = _FIXTURE_PATH) -> list[MetricRecord]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [MetricRecord.model_validate(row) for row in raw]


def list_metrics(fixture_path: Path | None = None) -> list[MetricRecord]:
    path = fixture_path or _FIXTURE_PATH
    return _load_records(path)


def evaluate_by_record_id(
    record_id: str, fixture_path: Path | None = None
) -> MetricEvaluation | None:
    path = fixture_path or _FIXTURE_PATH
    for row in _load_records(path):
        if row.record_id != record_id:
            continue
        rec = recommend_for_metric(row.metric_name, row.metric_trend)
        return MetricEvaluation(
            record_id=row.record_id,
            portfolio_name=row.portfolio_name,
            metric_name=row.metric_name,
            metric_value=row.metric_value,
            metric_trend=row.metric_trend,
            analysis_finding=row.analysis_finding,
            recommendation=rec,
        )
    return None
