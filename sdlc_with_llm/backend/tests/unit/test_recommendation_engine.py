"""Domain: recommendations derived from analysed metric trend and name (no persistence)."""

import pytest

from app.domain.recommendation_engine import recommend_for_metric


@pytest.mark.parametrize(
    ("metric_name", "metric_trend", "expected"),
    [
        (
            "Revenue Growth",
            "Increasing",
            "Consider maintaining current allocation due to positive revenue growth trend.",
        ),
        (
            "Profit Margin",
            "Stable",
            "Continue monitoring margin performance and maintain current strategy.",
        ),
        (
            "Expense Ratio",
            "Increasing",
            "Review cost structure to identify opportunities for reducing expenses.",
        ),
        (
            "Return on Investment",
            "Decreasing",
            "Assess underperforming areas and consider rebalancing where appropriate.",
        ),
        (
            "Cash Flow",
            "Increasing",
            "Consider using improved cash flow to support future investment decisions.",
        ),
    ],
)
def test_recommendation_matches_acceptance_fixtures(
    metric_name: str, metric_trend: str, expected: str
) -> None:
    assert recommend_for_metric(metric_name, metric_trend) == expected


def test_unknown_metric_falls_back_to_generic_guidance() -> None:
    out = recommend_for_metric("Custom Metric", "Stable")
    assert "Review" in out or "monitor" in out.lower()
