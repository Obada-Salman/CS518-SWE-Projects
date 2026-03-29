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

from Enemy import Enemy


class PotatoEnemyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("Enemy.SpriteHandler")
    def test_potato_enemy_uses_expected_defaults_and_sprite(self, mock_sprite_handler):
        sprite = Mock()
        sprite.get_current_frame.return_value = pygame.Surface((83, 94), pygame.SRCALPHA)
        mock_sprite_handler.return_value = sprite

        enemy = Enemy(10, 20, 83, 94, type="enemy_potato")

        self.assertEqual(enemy.type, "enemy_potato")
        self.assertEqual(enemy.speed, 2)
        self.assertEqual(enemy.health, 5)
        self.assertEqual(enemy.max_health, 5)
        self.assertEqual(enemy.vx, -2)
        mock_sprite_handler.assert_called_once_with(
            "assets/images/Characters/Potato_83x94.png", type="enemy_potato"
        )

    @patch("Enemy.SpriteHandler")
    def test_potato_enemy_allows_speed_override(self, mock_sprite_handler):
        sprite = Mock()
        sprite.get_current_frame.return_value = pygame.Surface((83, 94), pygame.SRCALPHA)
        mock_sprite_handler.return_value = sprite

        enemy = Enemy(10, 20, 83, 94, type="enemy_potato", speed=7)

        self.assertEqual(enemy.speed, 7)
        self.assertEqual(enemy.vx, -7)
        self.assertEqual(enemy.health, 5)

    @patch("Enemy.SpriteHandler")
    def test_potato_enemy_update_moves_dead_enemy_offscreen(self, mock_sprite_handler):
        sprite = Mock()
        sprite.get_current_frame.return_value = pygame.Surface((83, 94), pygame.SRCALPHA)
        mock_sprite_handler.return_value = sprite

        enemy = Enemy(10, 20, 83, 94, type="enemy_potato")
        enemy.health = 0
        game_map = [[None]]

        enemy.update(game_map, tile_size=32)

        self.assertEqual(enemy.rect.topleft, (-1000, -1000))
        sprite.update.assert_called_once_with(direction=enemy.direction, state=enemy.state)


if __name__ == "__main__":
    unittest.main()