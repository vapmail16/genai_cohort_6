import { describe, expect, it } from "vitest";
import type { Evaluation } from "../../src/domain/evaluation";
import {
  evaluationHeadline,
  recommendationOnlyCopy,
} from "../../src/domain/evaluationPresentation";

const sample: Evaluation = {
  record_id: "SD-US3-005",
  portfolio_name: "Multi-Asset Growth Portfolio",
  metric_name: "Cash Flow",
  metric_value: "£250,000",
  metric_trend: "Increasing",
  analysis_finding: "Cash flow position has strengthened.",
  recommendation: "Consider using improved cash flow.",
};

describe("evaluationPresentation", () => {
  it("builds headline from metric and portfolio", () => {
    expect(evaluationHeadline(sample)).toBe(
      "Cash Flow — Multi-Asset Growth Portfolio"
    );
  });

  it("surfaces readable recommendation snippet for UI teaser", () => {
    expect(recommendationOnlyCopy(sample)).toBe(
      "Consider using improved cash flow."
    );
  });
});
