/** API row shape from GET /api/metrics (finding only; recommendation from evaluation). */

export type MetricRow = {
  record_id: string;
  user_role: string;
  portfolio_name: string;
  metric_name: string;
  metric_value: string;
  metric_trend: string;
  analysis_finding: string;
};

export type Evaluation = MetricRow & { recommendation: string };
