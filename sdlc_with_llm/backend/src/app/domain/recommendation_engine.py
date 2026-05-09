def recommend_for_metric(metric_name: str, metric_trend: str) -> str:
    key = (metric_name.strip().lower(), metric_trend.strip().lower())
    table: dict[tuple[str, str], str] = {
        (
            "revenue growth",
            "increasing",
        ): "Consider maintaining current allocation due to positive revenue growth trend.",
        (
            "profit margin",
            "stable",
        ): "Continue monitoring margin performance and maintain current strategy.",
        (
            "expense ratio",
            "increasing",
        ): "Review cost structure to identify opportunities for reducing expenses.",
        (
            "return on investment",
            "decreasing",
        ): "Assess underperforming areas and consider rebalancing where appropriate.",
        (
            "cash flow",
            "increasing",
        ): "Consider using improved cash flow to support future investment decisions.",
    }
    if key in table:
        return table[key]
    return "Continue monitoring metric performance and review periodically based on stakeholder guidance."
