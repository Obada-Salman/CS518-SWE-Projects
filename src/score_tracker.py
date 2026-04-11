from __future__ import annotations

from dataclasses import dataclass
import os
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
        self.server_url = os.getenv("LEADERBOARD_SERVER_URL", server_url)
        self.username = username
        self.total_score = 0
        self.level_score = 0
        self.enemy_kills = 0
        self.resources_collected = 0
        self.current_level: str | None = None
        self.level_start_ms = pygame.time.get_ticks()
        self._last_tick_ms = self.level_start_ms
        self._level_finalized = False

    def start_level(self, level_name: str) -> None:
        now = pygame.time.get_ticks()
        self.current_level = level_name
        self.level_score = 0
        self.enemy_kills = 0
        self.resources_collected = 0
        self.level_start_ms = now
        self._last_tick_ms = now
        self._level_finalized = False

    def add_points(self, points: int) -> None:
        if points <= 0:
            return
        self.level_score += points
        self.total_score += points

    def tick(self) -> None:
        # Reserved for future time-based effects.
        self._last_tick_ms = pygame.time.get_ticks()

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

    def finalize_level_completion(
        self,
        target_time_ms: int = 180_000,
        clear_bonus_points: int = 500,
        speed_points_per_100ms: int = 1,
    ) -> dict[str, int]:
        if self._level_finalized:
            return {
                "clear_bonus": 0,
                "speed_bonus": 0,
                "elapsed_ms": self.get_level_completion_time_ms(),
            }

        elapsed_ms = self.get_level_completion_time_ms()
        speed_bonus = 0
        if elapsed_ms < target_time_ms and speed_points_per_100ms > 0:
            speed_bonus = ((target_time_ms - elapsed_ms) // 100) * speed_points_per_100ms

        total_bonus = max(0, clear_bonus_points) + int(speed_bonus)
        if total_bonus > 0:
            self.add_points(total_bonus)

        self._level_finalized = True
        return {
            "clear_bonus": max(0, clear_bonus_points),
            "speed_bonus": int(speed_bonus),
            "elapsed_ms": elapsed_ms,
        }

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
