#!/usr/bin/env python3
"""
Test script to verify game components load correctly
This script tests imports without initializing pygame display
"""
import os
import sys

# Change to src directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set environment variable to use dummy video driver
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

try:
    print("Testing game component imports...")
    
    print("  - Importing constants...", end=" ")
    from src.constants import *
    print("✓")
    
    print("  - Importing platforms...", end=" ")
    from src.platforms import Platform, MovingPlatform
    print("✓")
    
    print("  - Importing enemies...", end=" ")
    from src.enemies import Enemy, Boss
    print("✓")
    
    print("  - Importing player...", end=" ")
    from src.player import Player
    print("✓")
    
    print("  - Importing levels...", end=" ")
    from src.levels import Level
    print("✓")
    
    print("  - Importing story...", end=" ")
    from src.story import StoryManager, Cutscene
    print("✓")
    
    print("  - Importing audio...", end=" ")
    from src.audio import init_sound_manager
    print("✓")
    
    print("  - Importing effects...", end=" ")
    from src.effects import ParticleSystem, ScreenShake, FloatingTextManager
    print("✓")
    
    print("\n✓ All components imported successfully!")
    print("\nGame structure:")
    print(f"  - Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"  - FPS: {FPS}")
    print(f"  - Gravity: {GRAVITY}")
    print(f"  - Max health: {PLAYER_MAX_HEALTH}")
    
except Exception as e:
    print(f"\n✗ Error importing components:")
    print(f"  {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
