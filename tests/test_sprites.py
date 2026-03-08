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

from SpriteHandler import SpriteHandler
from Player import Player
from Enemy import Enemy
from configs import CONFIGS
from settings import BASE_HEIGHT


class FakeKeys:
    def __init__(self, pressed=None):
        self.pressed = set(pressed or [])

    def __getitem__(self, key):
        return key in self.pressed


class SpriteHandlerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_parse_frames_respects_config_and_scale(self, mock_load):
        cfg = CONFIGS["player"]
        mock_sheet = pygame.Surface((cfg["frame_width"] * cfg["cols"], cfg["frame_height"]), pygame.SRCALPHA)
        mock_load.return_value = mock_sheet

        handler = SpriteHandler("unused.png", type="player", scale=2)

        self.assertEqual(len(handler._all_frames), cfg["cols"])
        self.assertTrue(all(frame.get_width() == cfg["frame_width"] * 2 for frame in handler._all_frames))

    @patch("pygame.image.load")
    def test_get_current_frames_uses_direction_and_state_animation_sets(self, mock_load):
        cfg = CONFIGS["enemy_carrot"]
        mock_sheet = pygame.Surface((cfg["frame_width"] * cfg["cols"], cfg["frame_height"]), pygame.SRCALPHA)
        mock_load.return_value = mock_sheet

        handler = SpriteHandler("unused.png", type="enemy_carrot")
        frames = handler.get_current_frames(direction=0, state=1)

        expected_indexes = cfg["animations"]["walk_left"]
        expected_frames = [handler._all_frames[i] for i in expected_indexes]
        self.assertEqual(frames, expected_frames)

    @patch("pygame.image.load")
    def test_update_advances_frames_and_resets_on_state_change(self, mock_load):
        cfg = CONFIGS["player"]
        mock_sheet = pygame.Surface((cfg["frame_width"] * cfg["cols"], cfg["frame_height"]), pygame.SRCALPHA)
        mock_load.return_value = mock_sheet

        handler = SpriteHandler("unused.png", type="player", anim_time=2)
        handler.update(state=0)
        handler.update(state=0)
        self.assertEqual(handler.frame_idx, 1)

        handler.update(state=1)
        self.assertEqual(handler.frame_idx, 0)
        self.assertEqual(handler.anim_counter, 1)


class PlayerSpriteAndPhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("Player.SpriteHandler")
    @patch("pygame.image.load")
    def test_apply_physics_lands_player_on_floor(self, mock_load, mock_sprite_handler):
        mock_load.return_value = pygame.Surface((34, 34), pygame.SRCALPHA)
        mock_sprite_handler.return_value = Mock()

        player = Player(20, 20, 34, 34)
        floor = BASE_HEIGHT - player.height
        player.y = floor + 5
        player.vy = 3

        player.apply_physics()

        self.assertEqual(player.y, floor)
        self.assertEqual(player.vy, 0.0)
        self.assertTrue(player.on_ground)

    @patch("Player.SpriteHandler")
    @patch("pygame.image.load")
    @patch("pygame.key.get_pressed")
    def test_handle_input_jump_sets_vertical_velocity_and_jump_state(self, mock_keys, mock_load, mock_sprite_handler):
        mock_load.return_value = pygame.Surface((34, 34), pygame.SRCALPHA)
        mock_sprite_handler.return_value = Mock()
        mock_keys.return_value = FakeKeys({pygame.K_UP})

        player = Player(10, 10, 34, 34)
        player.on_ground = True

        player.handle_input()

        self.assertEqual(player.vy, player.jump_strength)
        self.assertFalse(player.on_ground)
        self.assertEqual(player.state, 2)

    @patch("Player.SpriteHandler")
    @patch("pygame.image.load")
    @patch("pygame.key.get_pressed")
    def test_handle_input_shoots_only_once_when_x_held(self, mock_keys, mock_load, mock_sprite_handler):
        mock_load.return_value = pygame.Surface((34, 34), pygame.SRCALPHA)
        mock_sprite_handler.return_value = Mock()

        player = Player(10, 10, 34, 34)
        player.rect = pygame.Rect(10, 10, 34, 34)

        mock_keys.side_effect = [FakeKeys({pygame.K_x}), FakeKeys({pygame.K_x})]

        player.handle_input()
        player.handle_input()

        self.assertEqual(len(player.tears), 1)


class EnemySpriteAndPhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("Enemy.SpriteHandler")
    def test_apply_physics_bounces_off_left_edge_and_updates_direction(self, mock_sprite_handler):
        fake_sprite = Mock()
        mock_sprite_handler.return_value = fake_sprite

        enemy = Enemy(0, 50, 75, 110, speed=5)
        enemy.vx = -5

        enemy.apply_physics()

        self.assertEqual(enemy.x, 0)
        self.assertGreater(enemy.vx, 0)
        self.assertEqual(enemy.direction, 1)
        self.assertEqual(enemy.state, 1)

    @patch("Enemy.SpriteHandler")
    def test_update_passes_state_and_direction_to_sprite_handler(self, mock_sprite_handler):
        fake_sprite = Mock()
        mock_sprite_handler.return_value = fake_sprite

        enemy = Enemy(100, 50, 75, 110, speed=5)
        enemy.direction = 0
        enemy.state = 1

        enemy.update()

        fake_sprite.update.assert_called_once_with(direction=enemy.direction, state=enemy.state)


if __name__ == "__main__":
    unittest.main()
