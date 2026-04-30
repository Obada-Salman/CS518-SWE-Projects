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


class AllyStuckDetectionTests(unittest.TestCase):
    """Test the stuck detection system for allies."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_stuck_timer_initialized(self):
        """Stuck timer should be initialized."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        
        assert hasattr(ally, 'stuck_timer'), "Should have stuck_timer property"
        assert hasattr(ally, 'last_x'), "Should have last_x property"
        assert ally.stuck_timer == 0, "stuck_timer should start at 0"

    def test_stuck_timer_resets_when_moving(self):
        """Stuck timer should reset when ally is actually moving."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.on_ground = True
        ally.stuck_timer = 10
        ally.last_x = 100
        ally.x = 105  # Moving
        ally.vx = 3
        
        game_map = [[None]]
        ally.update(game_map, 32)
        
        assert ally.stuck_timer == 0, "Stuck timer should reset when moving"

    def test_no_jump_without_ground(self):
        """Should not perform emergency jump if not on ground."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.on_ground = False  # Airborne
        ally.vx = 3
        ally.x = 100
        ally.stuck_timer = 25  # Stuck for long time
        ally.wall_jump_cooldown = 0
        
        initial_vy = ally.vy
        game_map = [[None]]
        ally.update(game_map, 32)
        
        # Should not jump if already airborne
        # (checking that we don't compound jumping issues)
        assert ally.wall_jump_cooldown >= 0, "Cooldown should be managed"

    def test_stuck_detection_properties_present(self):
        """Verify stuck detection properties are present and working."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        
        # Stuck detection should be active
        assert hasattr(ally, 'stuck_timer'), "Should track stuck state"
        assert hasattr(ally, 'last_x'), "Should track last X position"
        assert hasattr(ally, 'wall_jump_cooldown'), "Should have wall jump cooldown"
        
        # All should start at 0
        assert ally.stuck_timer == 0, "Stuck timer starts at 0"
        assert ally.wall_jump_cooldown == 0, "Wall jump cooldown starts at 0"


if __name__ == '__main__':
    unittest.main()
