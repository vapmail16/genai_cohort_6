import { beforeEach, describe, expect, it, vi } from "vitest";
import { fetchEvaluation, fetchMetrics } from "../../src/api";
import type { Evaluation, MetricRow } from "../../src/domain/evaluation";

describe("api client", () => {
  beforeEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("fetchMetrics returns parsed rows", async () => {
    const rows: MetricRow[] = [
      {
        record_id: "SD-US3-001",
        user_role: "Portfolio Manager",
        portfolio_name: "P",
        metric_name: "M",
        metric_value: "1",
        metric_trend: "Stable",
        analysis_finding: "f",
      },
    ];
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json: async () => rows })
    );

    await expect(fetchMetrics()).resolves.toEqual(rows);
    expect(fetch).toHaveBeenCalledWith("/api/metrics");
  });

  it("fetchEvaluation encodes record id and returns evaluation", async () => {
    const body: Evaluation = {
      record_id: "SD-US3-002",
      user_role: "Portfolio Manager",
      portfolio_name: "P",
      metric_name: "M",
      metric_value: "2",
      metric_trend: "Increasing",
      analysis_finding: "x",
      recommendation: "y",
    };
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json: async () => body })
    );

    await expect(fetchEvaluation("SD/US3")).resolves.toEqual(body);
    expect(fetch).toHaveBeenCalledWith("/api/metrics/SD%2FUS3/evaluation");
  });
});
