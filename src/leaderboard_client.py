from __future__ import annotations

import json
from typing import Any, Optional
from urllib import request
from urllib.error import HTTPError, URLError


def submit_score(
    server_url: str,
    username: str,
    score: int,
    completion_time_ms: int,
    level_name: Optional[str] = None,
    timeout_seconds: int = 5,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "username": username,
        "score": score,
        "completion_time_ms": completion_time_ms,
    }

    if level_name:
        payload["level_name"] = level_name

    body = json.dumps(payload).encode("utf-8")

    req = request.Request(
        url=f"{server_url.rstrip('/')}/api/scores",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {error.code}: {detail}"}
    except URLError as error:
        return {"error": f"Connection error: {error.reason}"}
