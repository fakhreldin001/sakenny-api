"""
MLflow experiment tracking for Sakenny
Uses MLflow REST API directly - no mlflow package needed
"""

import os
import requests
from datetime import datetime

MLFLOW_URL = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")


def _get_or_create_experiment(name: str) -> str:
    """Get experiment ID by name, or create it if it doesn't exist."""
    try:
        resp = requests.get(f"{MLFLOW_URL}/api/2.0/mlflow/experiments/get-by-name", params={"experiment_name": name})
        if resp.status_code == 200:
            return resp.json()["experiment"]["experiment_id"]
        
        resp = requests.post(f"{MLFLOW_URL}/api/2.0/mlflow/experiments/create", json={"name": name})
        return resp.json()["experiment_id"]
    except Exception:
        return "0"


def _create_run(experiment_id: str, run_name: str) -> str:
    """Create a new run and return its ID."""
    resp = requests.post(f"{MLFLOW_URL}/api/2.0/mlflow/runs/create", json={
        "experiment_id": experiment_id,
        "run_name": run_name,
        "start_time": int(datetime.now().timestamp() * 1000)
    })
    return resp.json()["run"]["info"]["run_id"]


def _log_param(run_id: str, key: str, value: str):
    requests.post(f"{MLFLOW_URL}/api/2.0/mlflow/runs/log-parameter", json={
        "run_id": run_id, "key": key, "value": str(value)
    })


def _log_metric(run_id: str, key: str, value: float):
    requests.post(f"{MLFLOW_URL}/api/2.0/mlflow/runs/log-metric", json={
        "run_id": run_id, "key": key, "value": value, "timestamp": int(datetime.now().timestamp() * 1000)
    })


def _end_run(run_id: str):
    requests.post(f"{MLFLOW_URL}/api/2.0/mlflow/runs/update", json={
        "run_id": run_id, "status": "FINISHED", "end_time": int(datetime.now().timestamp() * 1000)
    })


def log_embedding_experiment(model_name: str, dimension: int, sample_text: str, embedding: list[float]):
    """Logs details about an embedding generation."""
    try:
        exp_id = _get_or_create_experiment("sakenny-embeddings")
        run_id = _create_run(exp_id, f"embed-{model_name}")
        _log_param(run_id, "model_name", model_name)
        _log_param(run_id, "dimension", str(dimension))
        _log_param(run_id, "sample_text_length", str(len(sample_text)))
        _log_metric(run_id, "embedding_dimension", dimension)
        _log_metric(run_id, "text_length", len(sample_text))
        _end_run(run_id)
    except Exception:
        pass


def log_search_experiment(query: str, num_results: int, top_score: float):
    """Logs details about a semantic search."""
    try:
        exp_id = _get_or_create_experiment("sakenny-search")
        run_id = _create_run(exp_id, "search")
        _log_param(run_id, "query", query)
        _log_metric(run_id, "num_results", num_results)
        _log_metric(run_id, "top_similarity_score", top_score)
        _end_run(run_id)
    except Exception:
        pass