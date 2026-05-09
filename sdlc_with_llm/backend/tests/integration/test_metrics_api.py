"""API layer: list and evaluate metrics from in-memory fixtures."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_list_metrics_returns_fixture_rows(client: TestClient) -> None:
    r = client.get("/api/metrics")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5
    assert data[0]["record_id"] == "SD-US3-001"


def test_evaluate_metric_returns_finding_and_recommendation(client: TestClient) -> None:
    r = client.get("/api/metrics/SD-US3-004/evaluation")
    assert r.status_code == 200
    body = r.json()
    assert body["record_id"] == "SD-US3-004"
    assert body["analysis_finding"]
    assert body["recommendation"] == (
        "Assess underperforming areas and consider rebalancing where appropriate."
    )


def test_evaluate_unknown_record_returns_404(client: TestClient) -> None:
    assert client.get("/api/metrics/unknown/evaluation").status_code == 404
