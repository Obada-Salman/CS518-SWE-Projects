import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from NPC import NPC
from StoryState import StoryState


class RecruitAndOnionAllyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_complete_recruitment_sets_recruited_and_speed_and_plays_sound(self):
        # Create an NPC ally and a minimal StoryState without running __init__
        ally = NPC(50, 60, 75, 110, type='carrot', team='ally')
        ally.recruited = False

        ss = StoryState.__new__(StoryState)
        ss.snd_collect = Mock()

        # Call the completion routine
        ss._complete_recruitment(ally)

        self.assertTrue(ally.recruited, "Ally should be marked recruited")
        self.assertEqual(ally.speed, 250.0, "Ally speed should be set to 250 on recruitment")
        ss.snd_collect.play.assert_called_once()

    def test_planting_pot_creates_onion_ally_when_resources_and_e_key(self):
        # Minimal StoryState instance (skip __init__ to avoid heavy resource loading)
        ss = StoryState.__new__(StoryState)
        ss.sequence_player = SimpleNamespace(active=False)

        # Minimal player with position near the pot
        player = SimpleNamespace()
        player.x = 100
        player.y = 100
        player.rect = pygame.Rect(player.x, player.y, 34, 34)
        player.mask = pygame.mask.Mask((1, 1))
        player.update = Mock()
        player.is_alive = lambda: True
        ss.player = player

        ss.map = [[None for _ in range(10)] for _ in range(10)]
        ss.tile_size = 32
        ss.ally_list = []
        ss.enemy_list = []

        # Put a pot very near the player so dist < 100
        pot = SimpleNamespace()
        pot.position = (player.x + 10, player.y + 10)
        ss.pot_list = [pot]

        # Mock state_machine to report sufficient resources and accept deductions
        class FakeStateMachine:
            def get_water_collected(self):
                return 5
            def get_sunlight_collected(self):
                return 3
            def get_nutrients_collected(self):
                return 2
            def add_water(self, v):
                pass
            def add_sunlight(self, v):
                pass
            def add_nutrients(self, v):
                pass
            def transition(self, name):
                pass

        ss.state_machine = FakeStateMachine()

        # Provide sound mock
        ss.snd_collect = Mock()

        # Ensure no enemies/alleys cause early returns
        ss.enemy_list = []
        ss.ally_list = []

        # Ensure key press for E is True by making a list with index K_e True
        key_state = [False] * 512
        key_state[pygame.K_e] = True

        orig_get_pressed = pygame.key.get_pressed
        pygame.key.get_pressed = lambda: key_state

        try:
            # Call update which contains the pot planting logic
            ss.true_width = 800
            ss.true_height = 600
            ss.scroll = 0
            ss.current_level = 1
            ss.snd_damage = Mock()
            ss.snd_tear_hit = Mock()
            ss.snd_collect = ss.snd_collect
            ss.collectibles = []
            ss.door = pygame.Rect(0, 0, 32, 32)
            ss.door_locked = True

            # Ensure attributes referenced later exist
            ss.spike_list = []
            ss.pot_list = ss.pot_list

            # Call update with empty events and small dt
            ss.update([], 0.016)

            # After update, an onion ally should have been created and marked recruited
            self.assertTrue(any(getattr(a, 'type', None) == 'onion' for a in ss.ally_list), "An onion ally should be created from the pot")
            onion = [a for a in ss.ally_list if getattr(a, 'type', None) == 'onion'][0]
            self.assertTrue(onion.recruited, "Onion ally should be recruited immediately when planted")
        finally:
            pygame.key.get_pressed = orig_get_pressed


if __name__ == '__main__':
    unittest.main()
