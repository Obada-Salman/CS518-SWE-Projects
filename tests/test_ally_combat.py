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


class AllyHealthBasedCombatTests(unittest.TestCase):
    """Test the health-based combat system for allies."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_healthier_ally_wins_combat(self):
        """Healthier ally should take less damage than weaker enemy."""
        # Create ally with 7 health (potato stats) and 2 damage
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.recruited = True
        ally.health = 7  # High health
        ally.damage = 2
        
        # Create enemy with 5 health (carrot stats) and 1 damage
        enemy = NPC(150, 100, 75, 110, type='carrot', team='enemy')
        enemy.health = 5  # Low health
        
        initial_ally_health = ally.health
        initial_enemy_health = enemy.health
        initial_ally_damage = ally.damage
        
        # Combat
        ally.combat_with(enemy)
        
        # Enemy should take full damage from ally
        assert enemy.health == initial_enemy_health - initial_ally_damage, "Enemy should take full damage"
        # Ally should take reduced damage (max(1, damage // 2))
        reduced_damage = max(1, initial_ally_damage // 2)
        assert ally.health == initial_ally_health - reduced_damage, "Ally should take reduced damage when winning"

    def test_weaker_ally_loses_combat(self):
        """Weaker ally should take more damage than healthier enemy."""
        # Create ally with 3 health (tomato stats) and 1 damage
        ally = NPC(100, 100, 94, 190, type='tomato', team='ally')
        ally.recruited = True
        ally.health = 3  # Low health
        
        # Create enemy with 12 health (pumpkin stats) and 3 damage
        enemy = NPC(150, 100, 94, 177, type='pumpkin', team='enemy')
        enemy.health = 12  # High health
        
        initial_ally_health = ally.health
        initial_enemy_health = enemy.health
        
        # Combat
        ally.combat_with(enemy)
        
        # Ally should take full damage, enemy takes reduced damage
        assert ally.health < initial_ally_health, "Ally should take damage when losing"
        assert enemy.health >= initial_enemy_health - (enemy.damage // 2), "Enemy should take reduced damage when winning"

    def test_equal_health_combat(self):
        """When health is equal, both should take full damage."""
        # Create two NPCs with same health
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.recruited = True
        ally.health = 5
        ally.damage = 2
        
        enemy = NPC(150, 100, 75, 110, type='carrot', team='enemy')
        enemy.health = 5
        enemy.damage = 1
        
        # Combat
        ally.combat_with(enemy)
        
        # Both should take damage
        assert ally.health < 5, "Ally should take damage"
        assert enemy.health < 5, "Enemy should take damage"

    def test_dead_characters_dont_combat(self):
        """Dead characters should not engage in combat."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.health = 0
        
        enemy = NPC(150, 100, 75, 110, type='carrot', team='enemy')
        enemy.health = 5
        
        initial_enemy_health = enemy.health
        
        # Combat with dead ally should do nothing
        ally.combat_with(enemy)
        
        # Enemy should not take damage
        assert enemy.health == initial_enemy_health, "Dead allies shouldn't deal damage"

    def test_ally_invincibility_after_combat(self):
        """Ally should become invincible after taking damage in combat."""
        ally = NPC(100, 100, 83, 94, type='potato', team='ally')
        ally.recruited = True
        ally.health = 3
        
        enemy = NPC(150, 100, 94, 177, type='pumpkin', team='enemy')
        enemy.health = 10
        
        # Before combat, ally is not invincible
        assert not ally.invincible, "Ally should not be invincible initially"
        
        # Combat
        ally.combat_with(enemy)
        
        # After combat where ally loses, ally should be invincible
        assert ally.invincible, "Ally should be invincible after taking damage"


if __name__ == '__main__':
    unittest.main()
