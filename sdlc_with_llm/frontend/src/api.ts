import type { Evaluation, MetricRow } from "./domain/evaluation";

export async function fetchMetrics(): Promise<MetricRow[]> {
  const res = await fetch("/api/metrics");
  if (!res.ok) {
    throw new Error(`Failed to load metrics (${res.status})`);
  }
  return res.json();
}

export async function fetchEvaluation(recordId: string): Promise<Evaluation> {
  const res = await fetch(`/api/metrics/${encodeURIComponent(recordId)}/evaluation`);
  if (res.status === 404) {
    throw new Error("Record not found");
  }
  if (!res.ok) {
    throw new Error(`Failed to evaluate (${res.status})`);
  }
  return res.json();
}
