from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pygame

from leaderboard_client import submit_score


@dataclass
class ScoreSnapshot:
    username: str
    current_level: str | None
    total_score: int
    level_score: int
    enemy_kills: int
    resources_collected: int
    elapsed_level_ms: int


class ScoreTracker:
    def __init__(self, server_url: str = "http://127.0.0.1:5000", username: str = "player1"):
        self.server_url = server_url
        self.username = username
        self.total_score = 0
        self.level_score = 0
        self.enemy_kills = 0
        self.resources_collected = 0
        self.current_level: str | None = None
        self.level_start_ms = pygame.time.get_ticks()
        self._last_tick_ms = self.level_start_ms

    def start_level(self, level_name: str) -> None:
        now = pygame.time.get_ticks()
        self.current_level = level_name
        self.level_score = 0
        self.enemy_kills = 0
        self.resources_collected = 0
        self.level_start_ms = now
        self._last_tick_ms = now

    def add_points(self, points: int) -> None:
        if points <= 0:
            return
        self.level_score += points
        self.total_score += points

    def tick(self) -> None:
        now = pygame.time.get_ticks()
        elapsed_ms = now - self._last_tick_ms
        if elapsed_ms <= 0:
            return

        # Baseline progression score so the system works even before combat/resources exist.
        baseline_points = elapsed_ms // 1000
        if baseline_points > 0:
            self.add_points(int(baseline_points))
            self._last_tick_ms += baseline_points * 1000

    def record_enemy_kill(self, points: int = 100) -> None:
        self.enemy_kills += 1
        self.add_points(points)

    def record_resource_collected(self, amount: int = 1, points_per_unit: int = 10) -> None:
        if amount <= 0:
            return
        self.resources_collected += amount
        self.add_points(amount * points_per_unit)

    def get_level_completion_time_ms(self) -> int:
        return max(0, pygame.time.get_ticks() - self.level_start_ms)

    def snapshot(self) -> ScoreSnapshot:
        return ScoreSnapshot(
            username=self.username,
            current_level=self.current_level,
            total_score=self.total_score,
            level_score=self.level_score,
            enemy_kills=self.enemy_kills,
            resources_collected=self.resources_collected,
            elapsed_level_ms=self.get_level_completion_time_ms(),
        )

    def submit_current_level(self, timeout_seconds: int = 2) -> dict[str, Any]:
        if not self.current_level:
            return {"error": "No active level to submit"}

        return submit_score(
            server_url=self.server_url,
            username=self.username,
            score=int(self.level_score),
            completion_time_ms=int(self.get_level_completion_time_ms()),
            level_name=self.current_level,
            timeout_seconds=timeout_seconds,
        )
