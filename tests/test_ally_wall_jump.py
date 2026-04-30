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

from NPC import NPC


class AllyWallJumpTests(unittest.TestCase):
    """Test the wall jump system for allies to escape being stuck."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_wall_state_initialized(self):
        """Wall jump properties should be initialized."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        
        assert hasattr(ally, 'on_wall'), "Should have on_wall property"
        assert hasattr(ally, 'wall_direction'), "Should have wall_direction property"
        assert hasattr(ally, 'wall_jump_cooldown'), "Should have wall_jump_cooldown property"
        assert ally.on_wall == False, "on_wall should start as False"
        assert ally.wall_direction == 0, "wall_direction should start as 0"
        assert ally.wall_jump_cooldown == 0, "wall_jump_cooldown should start as 0"

    def test_perform_wall_jump(self):
        """Wall jump should apply upward velocity and push away from wall."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.on_wall = True
        ally.wall_direction = 0  # Left wall
        ally.speed = 3
        
        initial_vx = ally.vx
        initial_vy = ally.vy
        
        # Perform wall jump
        ally.perform_wall_jump()
        
        # Should have upward velocity
        assert ally.vy < 0, "Wall jump should give upward velocity"
        assert ally.vy == -14.0, "Wall jump should have specific strength"
        
        # Should have horizontal velocity away from wall
        assert ally.vx == ally.speed, "Should move away from left wall (direction 0)"
        
        # Should set cooldown
        assert ally.wall_jump_cooldown == 15, "Should have wall jump cooldown"
        
        # Should turn off wall flag
        assert ally.on_wall == False, "Should turn off on_wall after jumping"

    def test_wall_jump_direction_right_wall(self):
        """Wall jump from right wall should push left."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.on_wall = True
        ally.wall_direction = 1  # Right wall
        ally.speed = 3
        
        ally.perform_wall_jump()
        
        # Should move left (negative velocity) away from right wall
        assert ally.vx == -ally.speed, "Should move away from right wall (direction 1)"

    def test_wall_jump_cooldown_decrements(self):
        """Wall jump cooldown should decrement each frame."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.wall_jump_cooldown = 10
        
        # Create minimal game map
        game_map = [[None]]
        
        initial_cooldown = ally.wall_jump_cooldown
        ally.update(game_map, 32)
        
        # Cooldown should decrement
        assert ally.wall_jump_cooldown == initial_cooldown - 1, "Cooldown should decrease by 1"

    def test_wall_flag_resets_each_frame(self):
        """on_wall flag should reset at start of each update."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.on_wall = True
        
        game_map = [[None]]
        ally.update(game_map, 32)
        
        # on_wall should be reset to False at start of update (only set if collision detected)
        assert ally.on_wall == False, "on_wall should reset each frame"


if __name__ == '__main__':
    unittest.main()
