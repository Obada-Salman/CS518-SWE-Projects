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

from PauseState import PauseState
from StoryState import StoryState
from state_manager import StateManager
from Menu import MainMenuState


class StoryPauseTransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("StoryState.pygame.mixer.Sound")
    @patch("StoryState.pygame.image.load")
    def test_story_escape_transitions_to_pause(self, mock_load, mock_sound):
        mock_load.return_value = pygame.Surface((10, 10), pygame.SRCALPHA)
        mock_sound.return_value = Mock()

        state_machine = Mock()
        state_machine.score_tracker = Mock()

        state = StoryState(state_machine)
        state.player = Mock()
        state.player.update = Mock()
        state.player.is_alive.return_value = True
        state.player.rect = pygame.Rect(0, 0, 20, 20)
        state.player.tears = []
        state.enemy_list = []
        state.ally_list = []
        state.collectibles = []
        state.map = [[None]]
        state.tile_size = 1
        state.door = pygame.Rect(100, 100, 10, 10)

        events = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})]
        state.update(events)

        state_machine.transition.assert_called_with("pause")
        state_machine.score_tracker.tick.assert_called_once()


class PauseStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_escape_resumes_story(self):
        state_machine = Mock()
        state_machine.states = {"story": Mock()}
        pause_state = PauseState("pause", state_machine)

        events = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})]
        pause_state.update(events)

        state_machine.transition.assert_called_once_with("story")

    def test_resume_button_transitions_to_story(self):
        state_machine = Mock()
        state_machine.states = {"story": Mock()}
        pause_state = PauseState("pause", state_machine)

        pause_state.btn_resume.is_clicked = Mock(return_value=True)
        pause_state.btn_levels.is_clicked = Mock(return_value=False)
        pause_state.btn_menu.is_clicked = Mock(return_value=False)

        events = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})]
        pause_state.update(events)

        state_machine.transition.assert_called_once_with("story")

    def test_level_select_button_transitions_to_level_select(self):
        state_machine = Mock()
        state_machine.states = {"story": Mock()}
        pause_state = PauseState("pause", state_machine)

        pause_state.btn_resume.is_clicked = Mock(return_value=False)
        pause_state.btn_levels.is_clicked = Mock(return_value=True)
        pause_state.btn_menu.is_clicked = Mock(return_value=False)

        events = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})]
        pause_state.update(events)

        state_machine.transition.assert_called_once_with("level_select")

    def test_main_menu_button_transitions_to_menu(self):
        state_machine = Mock()
        state_machine.states = {"story": Mock()}
        pause_state = PauseState("pause", state_machine)

        pause_state.btn_resume.is_clicked = Mock(return_value=False)
        pause_state.btn_levels.is_clicked = Mock(return_value=False)
        pause_state.btn_menu.is_clicked = Mock(return_value=True)

        events = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})]
        pause_state.update(events)

        state_machine.transition.assert_called_once_with("menu")

    def test_resize_rebuilds_pause_ui_and_story_ui(self):
        state_machine = Mock()
        story_state = Mock()
        state_machine.states = {"story": story_state}
        pause_state = PauseState("pause", state_machine)
        pause_state.setup_ui = Mock()

        events = [
            pygame.event.Event(
                pygame.VIDEORESIZE,
                {"size": (1024, 768), "w": 1024, "h": 768},
            )
        ]
        pause_state.update(events)

        pause_state.setup_ui.assert_called_once()
        story_state.setup_ui.assert_called_once()


class PauseCollectiblePersistenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("state_manager.ScoreTracker")
    @patch("state_manager.SoundManager")
    def test_pause_resume_does_not_reset_global_collectible_totals(
        self, _mock_sound_manager_cls, _mock_score_tracker_cls
    ):
        state_machine = StateManager()
        story_state = Mock()
        state_machine.states = {"story": story_state}
        state_machine.current_state_name = "pause"

        state_machine.add_water(2)
        state_machine.add_sunlight(3)
        state_machine.add_nutrients(4)

        pause_state = PauseState("pause", state_machine)
        pause_state.btn_resume.is_clicked = Mock(return_value=False)
        pause_state.btn_levels.is_clicked = Mock(return_value=False)
        pause_state.btn_menu.is_clicked = Mock(return_value=False)

        events = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})]
        pause_state.update(events)

        self.assertEqual(state_machine.current_state_name, "story")
        self.assertEqual(state_machine.get_water_collected(), 2)
        self.assertEqual(state_machine.get_sunlight_collected(), 3)
        self.assertEqual(state_machine.get_nutrients_collected(), 4)


class MenuUsernameInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1280, 720))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("Menu.pygame.image.load")
    def test_typing_username_applies_on_enter(self, mock_image_load):
        mock_image_load.return_value = pygame.Surface((50, 50), pygame.SRCALPHA)

        state_machine = Mock()
        state_machine.max_unlocked_level = 1
        state_machine.set_player_username = Mock(side_effect=lambda value: value.strip()[:32] if value.strip() else "player1")
        state_machine.score_tracker = Mock()
        state_machine.score_tracker.username = "player1"

        menu = MainMenuState("menu", state_machine)
        menu.story.is_clicked = Mock(return_value=False)
        menu.custom.is_clicked = Mock(return_value=False)
        menu.setting.is_clicked = Mock(return_value=False)
        menu.level_bld.is_clicked = Mock(return_value=False)
        menu.quit.is_clicked = Mock(return_value=False)

        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": menu.username_rect.center, "button": 1})
        key_j = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_j, "unicode": "J"})
        key_d = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d, "unicode": "D"})
        key_enter = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": ""})

        menu.username_input = ""
        menu.update([click_event, key_j, key_d, key_enter])

        state_machine.set_player_username.assert_called_with("JD")
        self.assertEqual(menu.username_input, "JD")

    @patch("Menu.pygame.image.load")
    def test_story_click_applies_default_username_when_blank(self, mock_image_load):
        mock_image_load.return_value = pygame.Surface((50, 50), pygame.SRCALPHA)

        state_machine = Mock()
        state_machine.max_unlocked_level = 1
        state_machine.set_player_username = Mock(return_value="player1")
        state_machine.score_tracker = Mock()
        state_machine.score_tracker.username = "player1"

        menu = MainMenuState("menu", state_machine)
        menu.username_input = "   "

        menu.story.is_clicked = Mock(return_value=True)
        menu.custom.is_clicked = Mock(return_value=False)
        menu.setting.is_clicked = Mock(return_value=False)
        menu.level_bld.is_clicked = Mock(return_value=False)
        menu.quit.is_clicked = Mock(return_value=False)

        click_story = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": menu.story.rect.center, "button": 1})
        menu.update([click_story])

        state_machine.set_player_username.assert_called_once()
        state_machine.transition.assert_called_once_with("level_select")


if __name__ == "__main__":
    unittest.main()