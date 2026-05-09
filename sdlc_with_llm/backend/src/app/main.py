from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.application.metrics_evaluation import evaluate_by_record_id, list_metrics

app = FastAPI(title="Financial Analysis Copilot (minimal)", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/metrics")
def get_metrics() -> list[dict]:
    return [m.model_dump() for m in list_metrics()]


@app.get("/api/metrics/{record_id}/evaluation")
def get_evaluation(record_id: str) -> dict:
    result = evaluate_by_record_id(record_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Metric record not found")
    return result.model_dump()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Financial Analysis Copilot API — see /docs"}
