import os
import sys
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from leaderboard_client import submit_score


class _FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class LeaderboardClientTests(unittest.TestCase):
    @patch("leaderboard_client.request.urlopen")
    def test_submit_score_handles_connection_reset(self, mock_urlopen):
        mock_urlopen.side_effect = ConnectionResetError(104, "Connection reset by peer")

        result = submit_score(
            server_url="http://127.0.0.1:5000",
            username="player1",
            score=100,
            completion_time_ms=1000,
            level_name="story_level_1",
        )

        self.assertIn("error", result)
        self.assertIn("Connection error", result["error"])

    @patch("leaderboard_client.request.urlopen")
    def test_submit_score_handles_invalid_json_response(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(b"not-json")

        result = submit_score(
            server_url="http://127.0.0.1:5000",
            username="player1",
            score=100,
            completion_time_ms=1000,
            level_name="story_level_1",
        )

        self.assertEqual(result, {"error": "Invalid JSON response from leaderboard server"})


if __name__ == "__main__":
    unittest.main()
