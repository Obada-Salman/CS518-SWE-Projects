import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from save_manager import SaveManager
from state_manager import StateManager


class SaveManagerTests(unittest.TestCase):
    def test_save_load_and_delete_slot_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("save_manager.get_user_data_path", return_value=temp_dir):
                saves = SaveManager(slot_count=3)
                payload = {
                    "username": "tester",
                    "max_unlocked_level": 6,
                    "water_collected": 4,
                    "sunlight_collected": 3,
                    "nutrients_collected": 2,
                    "current_story_level": 5,
                }

                saves.save_slot(2, payload)
                loaded = saves.load_slot(2)
                self.assertIsNotNone(loaded)
                self.assertEqual(loaded["username"], "tester")
                self.assertEqual(loaded["max_unlocked_level"], 6)
                self.assertIn("updated_at", loaded)

                deleted = saves.delete_slot(2)
                self.assertTrue(deleted)
                self.assertIsNone(saves.load_slot(2))


class _DummySaveManager:
    slot_count = 3

    def __init__(self):
        self.store = {}

    def load_slot(self, slot):
        return self.store.get(int(slot))

    def save_slot(self, slot, payload):
        self.store[int(slot)] = dict(payload)

    def delete_slot(self, slot):
        slot = int(slot)
        if slot in self.store:
            del self.store[slot]
            return True
        return False

    def list_slots(self):
        return []


class StateManagerSaveTests(unittest.TestCase):
    @patch("state_manager.ScoreTracker")
    @patch("state_manager.SoundManager")
    @patch("state_manager.SaveManager", new=_DummySaveManager)
    def test_create_new_game_and_quit_autosaves(self, _mock_sound_manager_cls, _mock_score_tracker_cls):
        state = StateManager()

        state.score_tracker.username = "player2"
        state.set_max_unlocked_level(7)
        state.add_water(4)
        state.add_sunlight(5)
        state.add_nutrients(6)

        saved = state.save_manager.store.get(state.active_save_slot)
        self.assertIsNotNone(saved)
        self.assertEqual(saved["max_unlocked_level"], 7)
        self.assertEqual(saved["water_collected"], 4)

        state.create_new_game(state.active_save_slot)
        self.assertEqual(state.max_unlocked_level, 1)
        self.assertEqual(state.get_water_collected(), 0)
        self.assertEqual(state.get_sunlight_collected(), 0)
        self.assertEqual(state.get_nutrients_collected(), 0)

        state.quit()
        self.assertTrue(state.window_should_close)


if __name__ == "__main__":
    unittest.main()
