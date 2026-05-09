import { fetchEvaluation, fetchMetrics } from "./api";
import type { Evaluation, MetricRow } from "./domain/evaluation";
import { evaluationHeadline } from "./domain/evaluationPresentation";

const root = document.querySelector("#table-root") as HTMLElement | null;
const detailEmpty = document.querySelector("#detail-empty") as HTMLElement | null;
const detailContent = document.querySelector("#detail-content") as HTMLElement | null;
const detailError = document.querySelector("#detail-error") as HTMLElement | null;

function renderTable(rows: MetricRow[]): void {
  if (!root) return;
  const thead = `<thead><tr>
    <th>Portfolio</th>
    <th>Metric</th>
    <th>Value</th>
    <th>Trend</th>
  </tr></thead>`;
  const body = rows
    .map(
      (r) =>
        `<tr data-selectable tabindex="0" data-id="${escapeHtml(r.record_id)}" aria-label="${
          escapeHtml(r.metric_name)} for ${escapeHtml(r.portfolio_name)}">
      <td>${escapeHtml(r.portfolio_name)}</td>
      <td>${escapeHtml(r.metric_name)}</td>
      <td>${escapeHtml(r.metric_value)}</td>
      <td>${escapeHtml(r.metric_trend)}</td>
    </tr>`
    )
    .join("");
  root.innerHTML = `<table>${thead}<tbody>${body}</tbody></table>`;

  root.querySelectorAll<HTMLTableRowElement>("tr[data-selectable]").forEach((row) => {
    const id = row.dataset.id!;
    row.addEventListener("click", () => selectMetric(id));
    row.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" || ev.key === " ") {
        ev.preventDefault();
        selectMetric(id);
      }
    });
  });
}

function escapeHtml(raw: string): string {
  return raw
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function selectMetric(recordId: string): Promise<void> {
  highlightRow(recordId);
  if (!detailEmpty || !detailContent || !detailError || !root) return;
  detailError.hidden = true;
  detailError.textContent = "";
  detailContent.hidden = true;
  detailContent.innerHTML = "";
  detailEmpty.hidden = false;
  detailEmpty.textContent = "Loading evaluation…";

  try {
    const evalRow: Evaluation = await fetchEvaluation(recordId);
    detailEmpty.hidden = true;
    detailContent.hidden = false;
    detailContent.innerHTML = buildDetailHtml(evalRow);
  } catch (e) {
    detailEmpty.hidden = true;
    detailError.hidden = false;
    detailError.textContent =
      e instanceof Error ? e.message : "Could not load evaluation.";
  }
}

function buildDetailHtml(e: Evaluation): string {
  return `
    <p><strong>${escapeHtml(evaluationHeadline(e))}</strong></p>
    <p><span style="color:#64748b">Value</span> ${escapeHtml(e.metric_value)} ·
    <span style="color:#64748b">Trend</span> ${escapeHtml(e.metric_trend)}</p>
    <p><strong>Analysis finding</strong><br/>${escapeHtml(e.analysis_finding)}</p>
    <p><strong>Recommendation</strong><br/>${escapeHtml(e.recommendation)}</p>
  `;
}

function highlightRow(recordId: string): void {
  if (!root) return;
  root.querySelectorAll("tr[data-selectable]").forEach((tr) => {
    const el = tr as HTMLTableRowElement;
    if (el.dataset.id === recordId) {
      el.classList.add("selected");
    } else {
      el.classList.remove("selected");
    }
  });
}

async function bootstrap(): Promise<void> {
  if (!root || !detailEmpty) return;
  try {
    const rows = await fetchMetrics();
    renderTable(rows);
  } catch {
    root.innerHTML =
      '<p class="error">Unable to load metrics. Is the backend running on port 8000?</p>';
  }
}

bootstrap();
