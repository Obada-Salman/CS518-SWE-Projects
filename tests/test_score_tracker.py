import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from score_tracker import ScoreTracker
from StoryState import StoryState


class ScoreTrackerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("score_tracker.submit_score")
    @patch("score_tracker.pygame.time.get_ticks")
    def test_score_uses_kills_resources_and_speed_bonus(self, mock_ticks, mock_submit_score):
        # __init__, start_level, finalize/get completion time, submit/get completion time
        mock_ticks.side_effect = [1000, 1000, 61000, 61000]
        mock_submit_score.return_value = {"ok": True}

        tracker = ScoreTracker(server_url="http://localhost:5000", username="tester")
        tracker.start_level("story_level_1")

        tracker.record_enemy_kill(points=100)
        tracker.record_enemy_kill(points=120)
        tracker.record_resource_collected(amount=3, points_per_unit=20)

        bonus = tracker.finalize_level_completion(target_time_ms=120000, clear_bonus_points=500)

        self.assertEqual(bonus["elapsed_ms"], 60000)
        self.assertEqual(bonus["clear_bonus"], 500)
        self.assertEqual(bonus["speed_bonus"], 600)
        self.assertEqual(tracker.level_score, 1380)

        tracker.submit_current_level()

        mock_submit_score.assert_called_once_with(
            server_url="http://localhost:5000",
            username="tester",
            score=1380,
            completion_time_ms=60000,
            level_name="story_level_1",
            timeout_seconds=2,
        )

    @patch("score_tracker.pygame.time.get_ticks")
    def test_finalize_is_idempotent(self, mock_ticks):
        mock_ticks.side_effect = [500, 500, 1000, 1200]

        tracker = ScoreTracker()
        tracker.start_level("story_level_2")

        first = tracker.finalize_level_completion(target_time_ms=2000, clear_bonus_points=100)
        second = tracker.finalize_level_completion(target_time_ms=2000, clear_bonus_points=100)

        self.assertGreater(first["clear_bonus"] + first["speed_bonus"], 0)
        self.assertEqual(second["clear_bonus"], 0)
        self.assertEqual(second["speed_bonus"], 0)


class StoryStateScoreSubmissionTests(unittest.TestCase):
    def test_leave_submits_only_when_level_cleared(self):
        story = StoryState.__new__(StoryState)
        tracker = Mock()
        story.score_tracker = tracker

        story.current_level = 1
        story.level_cleared = False
        story.leave()
        tracker.submit_current_level.assert_not_called()

        story.level_cleared = True
        story.leave()
        tracker.submit_current_level.assert_called_once()


if __name__ == "__main__":
    unittest.main()
