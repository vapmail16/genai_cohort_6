# genai_cohort_6

Monorepo for Generative AI cohort exercises: medallion demo, SDLC metrics app, SaaS scaffolding, **Streamlit NN demo**, and **local Ollama** setup scripts.

---

## Repository layout

| Path | Description |
|------|-------------|
| [`data_engineering_demo/`](data_engineering_demo/) | SQLite → bronze/silver/gold (Pandas) → PostgreSQL warehouse, DQ, PII masking, CLI pipeline |
| [`sdlc_with_llm/`](sdlc_with_llm/) | FastAPI backend + Vite/TypeScript frontend; metrics evaluation API (in-memory fixtures) |
| [`saas_project_scaffolding/`](saas_project_scaffolding/) | Placeholder monorepo structure (see its [README](saas_project_scaffolding/README.md)) |
| [`neural_network_example/`](neural_network_example/) | Streamlit slides: next-word prediction with neural nets (install `requirements.txt`, `streamlit run app.py`) |
| [`offline_model_setup/`](offline_model_setup/) | Ollama local LLM helpers: `setup.sh`, `download_model.sh`, `test_connection.py`; see [`offline_model_setup/README.md`](offline_model_setup/README.md) |

---

## Prerequisites

- **Python** 3.10+ (per-project virtualenvs recommended)
- **Node.js** 18+ for `sdlc_with_llm/frontend`
- **PostgreSQL** for the data pipeline warehouse load (or use `--skip-warehouse`)

**Virtualenvs:** Create a `.venv` (or `venv`) in each project directory as needed. Those folders are **not** committed; the repo root [`.gitignore`](.gitignore) ignores them. Share dependencies via `requirements.txt` / `pyproject.toml` only.

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

## Neural network demo (`neural_network_example`)

Slides in Streamlit (next-word prediction). Use a dedicated virtualenv:

```bash
cd neural_network_example
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Offline Ollama (`offline_model_setup`)

Install Ollama, pull a small model (e.g. `llama3.2:3b`), verify the API:

```bash
cd offline_model_setup
./setup.sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python test_connection.py
python -m unittest test_env_paths -v
```

Logs: [`offline_model_setup/ISSUE_LOG`](offline_model_setup/ISSUE_LOG).

---

## License

Unless noted per subdirectory, content is for **education and demonstration** within the cohort context.
