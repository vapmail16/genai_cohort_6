# genai_cohort_6

Monorepo for Generative AI cohort exercises: a **data engineering medallion demo**, an **SDLC / LLM metrics** full-stack sample, and a **SaaS scaffolding** layout.

---

## Repository layout

| Path | Description |
|------|-------------|
| [`data_engineering_demo/`](data_engineering_demo/) | SQLite → bronze/silver/gold (Pandas) → PostgreSQL warehouse, DQ, PII masking, CLI pipeline |
| [`sdlc_with_llm/`](sdlc_with_llm/) | FastAPI backend + Vite/TypeScript frontend; metrics evaluation API (in-memory fixtures) |
| [`saas_project_scaffolding/`](saas_project_scaffolding/) | Placeholder monorepo structure (see its [README](saas_project_scaffolding/README.md)) |

---

## Prerequisites

- **Python** 3.10+ (per-project virtualenvs recommended)
- **Node.js** 18+ for `sdlc_with_llm/frontend`
- **PostgreSQL** for the data pipeline warehouse load (or use `--skip-warehouse`)

---

## Data engineering demo (`data_engineering_demo`)

Medallion-style ETL: seed SQLite (`≤100` rows fixture), ingest, bronze/silver/gold zones, data quality checks, governance (masked PII), reports, and load into PostgreSQL.

```bash
cd data_engineering_demo
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

**Local PostgreSQL (default client port 5432)** — bootstrap role/database once, then run:

```bash
python -m de_demo --bootstrap-instructions   # prints paths and example psql
psql -h 127.0.0.1 -p 5432 -U postgres -f postgres/bootstrap_local_roles.sql
python -m de_demo --rows 100
```

**Docker Compose** for Postgres (host port `5433` in this repo):

```bash
export WAREHOUSE_HOST_PORT=5433
docker compose up -d
python -m de_demo --rows 100
```

**Without Postgres** (parquet + reports only):

```bash
python -m de_demo --rows 100 --skip-warehouse
```

**Tests:**

```bash
pytest
```

More detail: [`data_engineering_demo/ISSUE_LOG`](data_engineering_demo/ISSUE_LOG) (how-to and known pitfalls).

---

## SDLC + LLM app (`sdlc_with_llm`)

Backend exposes metrics evaluation JSON; frontend proxies `/api` to the API.

**Terminal 1 — API**

```bash
cd sdlc_with_llm/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --app-dir src --port 8000
```

**Terminal 2 — UI**

```bash
cd sdlc_with_llm/frontend
npm install && npm run dev
```

Open **http://localhost:5173** and use the metric UI to load `/api/metrics/{id}/evaluation`.

See also [`sdlc_with_llm/ISSUE_LOG`](sdlc_with_llm/ISSUE_LOG).

---

## License

Unless noted per subdirectory, content is for **education and demonstration** within the cohort context.
