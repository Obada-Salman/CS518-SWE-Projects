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

from Menu import MainMenuState
from StoryState import StoryState
from story_content import RECRUIT_DIALOGUE_BANK


class StoryStatePathfindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_find_path_routes_around_blocked_tile(self):
        state = StoryState.__new__(StoryState)
        state.tile_size = 32

        class Tile:
            def __init__(self, collision):
                self.collision = collision

        state.map = [
            [None, Tile(True), None],
            [None, None, None],
            [None, None, None],
        ]

        path = StoryState._find_path(state, (0, 0), (2, 0))

        self.assertIsNotNone(path)
        self.assertGreater(len(path), 3)
        self.assertNotIn((1, 0), path)

    def test_recruit_dialogue_includes_all_ally_types(self):
        for ally_type in ("carrot", "potato", "onion", "tomato", "bokchoy", "pumpkin", "broccoli"):
            self.assertIn(ally_type, RECRUIT_DIALOGUE_BANK)
            self.assertGreaterEqual(len(RECRUIT_DIALOGUE_BANK[ally_type]), 3)


class MenuSaveLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1280, 720))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("Menu.pygame.image.load")
    def test_save_controls_are_spaced_inside_panel(self, mock_image_load):
        mock_image_load.return_value = pygame.Surface((50, 50), pygame.SRCALPHA)

        state_machine = Mock()
        state_machine.max_unlocked_level = 1
        state_machine.set_player_username = Mock(return_value="player1")
        state_machine.score_tracker = Mock()
        state_machine.score_tracker.username = "player1"
        state_machine.save_manager = Mock()
        state_machine.save_manager.slot_count = 3
        state_machine.get_save_slots = Mock(return_value=[])

        menu = MainMenuState("menu", state_machine)

        self.assertFalse(menu.slot_prev.rect.colliderect(menu.btn_load_save.rect))
        self.assertFalse(menu.slot_next.rect.colliderect(menu.btn_load_save.rect))
        self.assertFalse(menu.btn_load_save.rect.colliderect(menu.btn_new_game.rect))
        self.assertFalse(menu.btn_new_game.rect.colliderect(menu.btn_delete_save.rect))
        self.assertTrue(menu.save_panel_rect.contains(menu.btn_load_save.rect))
        self.assertTrue(menu.save_panel_rect.contains(menu.btn_new_game.rect))
        self.assertTrue(menu.save_panel_rect.contains(menu.btn_delete_save.rect))


if __name__ == "__main__":
    unittest.main()
