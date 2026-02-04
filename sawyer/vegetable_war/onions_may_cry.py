#!/usr/bin/env python3
"""
Onions May Cry - The Vegetable War
A 2D platformer/fighting game where you defend your garden as an onion.
"""
import os
import sys

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

# Change working directory to src so relative imports work
os.chdir(src_dir)

# Now run the game
from main import Game

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
