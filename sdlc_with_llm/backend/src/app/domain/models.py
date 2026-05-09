from pydantic import BaseModel, Field


class MetricRecord(BaseModel):
    record_id: str = Field(..., examples=["SD-US3-001"])
    user_role: str
    portfolio_name: str
    metric_name: str
    metric_value: str
    metric_trend: str
    analysis_finding: str


class MetricEvaluation(BaseModel):
    record_id: str
    portfolio_name: str
    metric_name: str
    metric_value: str
    metric_trend: str
    analysis_finding: str
    recommendation: str
