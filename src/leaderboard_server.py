from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask, render_template, request

try:
    from leaderboard_db import LeaderboardRepository
except ModuleNotFoundError:
    from src.leaderboard_db import LeaderboardRepository


app = Flask(__name__)


def _resolve_db_path() -> Path | None:
    configured_path = os.getenv("LEADERBOARD_DB_PATH")
    if configured_path:
        return Path(configured_path)
    return None


repository = LeaderboardRepository(_resolve_db_path())


def _validate_payload(payload: dict[str, Any]) -> tuple[bool, str | None]:
    username = payload.get("username")
    if not isinstance(username, str) or not username.strip() or username == "":
        return False, "username must be a non-empty string"
    if len(username.strip()) > 32:
        return False, "username must be 32 characters or fewer"

    score = payload.get("score")
    if not isinstance(score, int) or score < 0:
        return False, "score must be a non-negative integer"

    completion_time_ms = payload.get("completion_time_ms")
    if not isinstance(completion_time_ms, int) or completion_time_ms < 0:
        return False, "completion_time_ms must be a non-negative integer"

    level_name = payload.get("level_name")
    if not isinstance(level_name, str) or not level_name.strip() or level_name == "":
        return False, "level_name must be a string when provided"

    return True, None


def _add_rank(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    for index, entry in enumerate(entries, start=1):
        ranked_entry = dict(entry)
        ranked_entry["rank"] = index
        ranked.append(ranked_entry)
    return ranked


@app.get("/")
def leaderboard_page() -> str:
    entries = _add_rank(repository.list_entries(limit=50))
    return render_template("leaderboard.html", entries=entries)


@app.get("/api/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@app.get("/api/scores")
def get_scores() -> tuple[dict[str, Any], int]:
    limit_raw = request.args.get("limit", "25")
    level_name = request.args.get("level_name")

    try:
        limit = int(limit_raw)
    except ValueError:
        return {"error": "limit must be an integer"}, 400

    entries = _add_rank(repository.list_entries(limit=limit, level_name=level_name))
    return {"entries": entries, "count": len(entries)}, 200


@app.post("/api/scores")
def post_score() -> tuple[dict[str, Any], int]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {"error": "request body must be valid JSON"}, 400

    is_valid, error_message = _validate_payload(payload)
    if not is_valid:
        return {"error": error_message}, 400

    saved_entry = repository.add_entry(
        username=payload["username"],
        score=payload["score"],
        completion_time_ms=payload["completion_time_ms"],
        level_name=payload.get("level_name"),
    )

    return {"entry": saved_entry}, 201


if __name__ == "__main__":
    host = os.getenv("LEADERBOARD_HOST", "127.0.0.1")
    port = int(os.getenv("LEADERBOARD_PORT", "5000"))
    debug = os.getenv("LEADERBOARD_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
