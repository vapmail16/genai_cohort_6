import type { Evaluation } from "./evaluation";

export function evaluationHeadline(row: Evaluation): string {
  return `${row.metric_name} — ${row.portfolio_name}`;
}

export function recommendationOnlyCopy(row: Evaluation): string {
  return row.recommendation.trim();
}
