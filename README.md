# genai_cohort_6

Monorepo for Generative AI cohort exercises: medallion demo, SDLC metrics app, SaaS scaffolding, **Streamlit NN demo**, **prompt engineering labs**, **LangChain + OpenAI** exercises, **vector database and RAG labs**, **OpenAI API smoke test**, and **local Ollama** setup scripts.

---

## Repository layout

| Path | Description |
|------|-------------|
| [`data_engineering_demo/`](data_engineering_demo/) | SQLite → bronze/silver/gold (Pandas) → PostgreSQL warehouse, DQ, PII masking, CLI pipeline |
| [`sdlc_with_llm/`](sdlc_with_llm/) | FastAPI backend + Vite/TypeScript frontend; metrics evaluation API (in-memory fixtures) |
| [`saas_project_scaffolding/`](saas_project_scaffolding/) | Placeholder monorepo structure (see its [README](saas_project_scaffolding/README.md)) |
| [`neural_network_example/`](neural_network_example/) | Streamlit slides: next-word prediction with neural nets (install `requirements.txt`, `streamlit run app.py`) |
| [`offline_model_setup/`](offline_model_setup/) | Ollama local LLM helpers: `setup.sh`, `download_model.sh`, `test_connection.py`; see [`offline_model_setup/README.md`](offline_model_setup/README.md) |
| [`prompt_engineering/`](prompt_engineering/) | Prompt techniques, injection, and token/temperature labs; see [`prompt_engineering/README.md`](prompt_engineering/README.md) |
| [`langchain_openai/`](langchain_openai/) | Week 2 LangChain scripts (chains, memory, model switch, chatbot); see [`langchain_openai/README.md`](langchain_openai/README.md) |
| [`ai_agents/`](ai_agents/) | LangGraph training demos (basic graphs, messages, tools, ReACT, memory); see [`ai_agents/langgraph_training_guide.md`](ai_agents/langgraph_training_guide.md) |
| [`vector_db_understanding/`](vector_db_understanding/) | Streamlit + Qdrant vector DB tutorial and PDF ingestion lab; see [`vector_db_understanding/README.md`](vector_db_understanding/README.md) |
| [`rag_understanding/`](rag_understanding/) | Streamlit RAG tutorial with retrieval and answer-generation demos; see [`rag_understanding/README.md`](rag_understanding/README.md) |
| [`openai_api_test/`](openai_api_test/) | Minimal script to verify `OPENAI_API_KEY` and API connectivity; see [`openai_api_test/README.md`](openai_api_test/README.md) |
| [`oxford_capstone/`](oxford_capstone/) | IT Support Agent capstone + MCP session bundle (`capstone_project/`, `mcp/`); see [`oxford_capstone/README.md`](oxford_capstone/README.md) |

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

## LangChain + OpenAI (`langchain_openai`)

Progressive scripts: basic LCEL chain, memory, multi-provider switch (OpenAI / Anthropic / Ollama), interactive chatbot, sequential chain.

```bash
cd langchain_openai
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Copy .env.example to .env and set OPENAI_API_KEY (and optional ANTHROPIC_API_KEY).
python 01_basic_chain.py
```

Full walkthrough: [`langchain_openai/README.md`](langchain_openai/README.md).

---

## AI agents (`ai_agents`)

LangGraph-focused agent training demos and walkthrough (`01_basic_graph` through `06_real_world_project`).

```bash
cd ai_agents
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python test_setup.py
python demos/01_basic_graph/activity_selector.py
```

Set `OPENAI_API_KEY` in repo root `.env` (or local `ai_agents/.env`).

---

## Prompt engineering (`prompt_engineering`)

Hands-on scripts for prompting basics, prompt injection, and token/temperature behavior.

```bash
cd prompt_engineering
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python 01_prompt_techniques.py
```

Uses env values from repo root `.env` (or local `prompt_engineering/.env` if present).

---

## Vector DB understanding (`vector_db_understanding`)

Interactive vector database tutorial plus PDF->Qdrant ingestion lab.

```bash
cd vector_db_understanding
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Set `QDRANT_URL`, `QDRANT_API_KEY`, and optional `QDRANT_COLLECTION` in repo root `.env` (or local `vector_db_understanding/.env`).

---

## RAG understanding (`rag_understanding`)

Interactive RAG concepts + live retrieval and generation demos.

```bash
cd rag_understanding
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Set `OPENAI_API_KEY` and Qdrant vars in repo root `.env` (or local `rag_understanding/.env`).

---

## OpenAI API test (`openai_api_test`)

Quick connectivity check against the OpenAI API.

```bash
cd openai_api_test
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m unittest test_env_paths -v
python test_openai.py
```

Set `OPENAI_API_KEY` in repo root `.env`, `openai_api_test/.env` (e.g. copy [`.env.example`](.env.example)), or `oxford_capstone/capstone_project/backend/.env` if you use that layout. See [`openai_api_test/README.md`](openai_api_test/README.md).

---

## Oxford bundle (`oxford_capstone`)

Self-contained IT Support Agent capstone plus MCP teaching assets:

| Subfolder | Purpose |
|-----------|---------|
| `oxford_capstone/capstone_project/` | FastAPI backend, React UI, Qdrant RAG, SQLite tickets, TypeScript MCP server |
| `oxford_capstone/mcp/` | Architecture HTML, MCP dungeon demo, session PDF |

```bash
cd oxford_capstone/capstone_project
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env   # set OPENAI_API_KEY
python -m backend.seed_demo_data --reset
python -m backend.rag.ingest --reset

# Terminal 1 — API
python3 -m uvicorn backend.main:app --reload --port 8000

# Terminal 2 — UI
cd frontend && npm install && npm run dev   # http://localhost:5173

# Terminal 3 — MCP server deps (Agentic MCP track)
cd ../mcp_server && npm install

# Tests
pytest

# Optional — architecture HTML (serve locally; see oxford_capstone/README.md)
cd ../../mcp && python3 -m http.server 8765

# Optional — MCP dungeon demo
cd mcp-dungeon && npm install && npm start   # http://localhost:3333
```

See [`oxford_capstone/README.md`](oxford_capstone/README.md) and [`oxford_capstone/capstone_project/docs/README.md`](oxford_capstone/capstone_project/docs/README.md).

---

## License

Unless noted per subdirectory, content is for **education and demonstration** within the cohort context.
