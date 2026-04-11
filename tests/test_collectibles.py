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

from StoryState import StoryState
from state_manager import StateManager


class CollectibleFeatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def _build_story_state(self, state_machine, collectibles):
        state = StoryState.__new__(StoryState)
        state.state_machine = state_machine
        state.current_level = 1
        state.level_cleared = False
        state.score_tracker = Mock()
        state.true_width = 200
        state.true_height = 200
        state.internal_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        state.scaled_width = 200
        state.scaled_height = 200
        state.offset_x = 0
        state.offset_y = 0
        state.scroll = 0
        state.ally_list = []

        player = Mock()
        player.rect = pygame.Rect(0, 0, 200, 200)
        player.tears = []
        player.update = Mock()
        player.is_alive.return_value = True
        state.player = player

        state.enemy_list = []
        state.map = [[None]]
        state.tile_size = 32
        state.door = pygame.Rect(300, 300, 32, 32)

        state.collectibles = list(collectibles)
        state.collectible_images = {
            "water": pygame.Surface((12, 12), pygame.SRCALPHA),
            "sunlight": pygame.Surface((12, 12), pygame.SRCALPHA),
            "nutrient": pygame.Surface((12, 12), pygame.SRCALPHA),
        }

        state.scaled_bg = pygame.Surface((200, 200), pygame.SRCALPHA)
        state.door_image = pygame.Surface((10, 10), pygame.SRCALPHA)
        state.lock_image = pygame.Surface((10, 10), pygame.SRCALPHA)
        state.door_locked = False

        return state

    @patch("state_manager.ScoreTracker")
    @patch("state_manager.SoundManager")
    @patch("StoryState.pygame.mixer.Sound")
    def test_collectibles_accumulate_globally_across_story_states(
        self, mock_sound_ctor, _mock_sound_manager_cls, _mock_score_tracker_cls
    ):
        mock_sound = Mock()
        mock_sound_ctor.return_value = mock_sound

        state_machine = StateManager()

        level_one_collectibles = [
            {"type": "water", "rect": pygame.Rect(10, 10, 20, 20)},
            {"type": "sunlight", "rect": pygame.Rect(40, 10, 20, 20)},
        ]
        level_two_collectibles = [
            {"type": "water", "rect": pygame.Rect(10, 10, 20, 20)},
            {"type": "nutrient", "rect": pygame.Rect(40, 10, 20, 20)},
        ]

        level_one_state = self._build_story_state(state_machine, level_one_collectibles)
        level_two_state = self._build_story_state(state_machine, level_two_collectibles)

        level_one_state.update([])
        level_two_state.update([])

        self.assertEqual(state_machine.get_water_collected(), 2)
        self.assertEqual(state_machine.get_sunlight_collected(), 1)
        self.assertEqual(state_machine.get_nutrients_collected(), 1)
        self.assertEqual(mock_sound.play.call_count, 4)

    @patch("state_manager.ScoreTracker")
    @patch("state_manager.SoundManager")
    @patch("StoryState.pygame.mixer.Sound")
    def test_collecting_resource_plays_collect_sound_once(
        self, mock_sound_ctor, _mock_sound_manager_cls, _mock_score_tracker_cls
    ):
        mock_sound = Mock()
        mock_sound_ctor.return_value = mock_sound

        state_machine = StateManager()
        collectibles = [{"type": "water", "rect": pygame.Rect(10, 10, 20, 20)}]
        state = self._build_story_state(state_machine, collectibles)

        state.update([])

        mock_sound_ctor.assert_called_once_with("assets/sounds/collect.ogg")
        mock_sound.play.assert_called_once()

    @patch("StoryState.game_map.draw_map")
    @patch("StoryState.math.sin")
    @patch("StoryState.pygame.time.get_ticks")
    def test_draw_applies_floating_offset_to_collectible_sprite(
        self, mock_ticks, mock_sin, mock_draw_map
    ):
        mock_ticks.return_value = 1234
        mock_sin.return_value = 0.5
        mock_draw_map.return_value = None

        state_machine = Mock()
        state = StoryState.__new__(StoryState)
        state.state_machine = state_machine
        state.true_width = 200
        state.true_height = 200
        state.internal_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        state.scaled_width = 200
        state.scaled_height = 200
        state.offset_x = 0
        state.offset_y = 0
        state.scroll = 0
        state.scaled_bg = pygame.Surface((200, 200), pygame.SRCALPHA)
        state.map = [[None]]
        state.tile_size = 32
        state.door = pygame.Rect(100, 100, 20, 20)
        state.door_image = pygame.Surface((10, 10), pygame.SRCALPHA)
        state.lock_image = pygame.Surface((10, 10), pygame.SRCALPHA)
        state.door_locked = False

        collectible_rect = pygame.Rect(80, 90, 20, 20)
        sprite = pygame.Surface((12, 12), pygame.SRCALPHA)
        state.collectibles = [{"type": "water", "rect": collectible_rect}]
        state.collectible_images = {"water": sprite}

        state.player = Mock()
        state.player.draw = Mock()
        state.enemy_list = []
        state.ally_list = []

        surface = pygame.Surface((200, 200), pygame.SRCALPHA)

        state.draw(surface)

        mock_sin.assert_called_once_with(1234 * 0.007)
        state.player.draw.assert_called_once()


if __name__ == "__main__":
    unittest.main()
