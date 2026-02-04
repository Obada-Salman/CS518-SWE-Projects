# Quick Start Guide - Onions May Cry

## Installation (One-Time Setup)

```bash
# Navigate to the game directory
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

## Running the Game

### Method 1: Simple Python Command
```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war
python3 onions_may_cry.py
```

### Method 2: Using the Shell Script
```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war
chmod +x run.sh
./run.sh
```

### Method 3: Direct Source Execution
```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war/src
python3 main.py
```

## Basic Controls

| Key | Action |
|-----|--------|
| **A** | Move left |
| **D** | Move right |
| **W** | Jump |
| **SPACE** | Attack enemy |
| **SHIFT** | Super Attack (when emotion meter is FULL) |
| **ESC** | Quit game |

## Your First Game (Beginner Guide)

### Stage 1: Learning the Basics
1. **Press SPACE to start** through the menu
2. **Watch the story** - This tells you what's happening
3. **Move with A/D** - Get used to movement
4. **Jump with W** - Practice jumping on platforms
5. **Attack with SPACE** - Hit enemies to fill your emotion meter
6. **Defeat all beans** - Once gone, stage 1 is complete!

### Stage 2: Getting Faster
1. **Peas are quick** - Don't chase them, let them come to you
2. **Use moving platforms** - Time your jumps to ride them
3. **Build emotion** - Keep hitting enemies
4. **Super attack** - When meter is full (SHIFT), use it on grouped peas
5. **Clear the stage**

### Stage 3: The Final Battle
1. **Face the Giant Garlic** - A tough boss
2. **Beat it down** - Use super attacks when available
3. **Watch for patterns** - The boss gets harder as it loses health
4. **Survive** - Don't take unnecessary risks
5. **Victory!** - You win the game!

## Game Flow

```
Menu
  ↓
Intro Cutscene (Story)
  ↓
Stage 1 (Beans) → Story → Stage 2 (Peas) → Story → Stage 3 (Garlic Boss)
  ↓
Victory Cutscene (You win!)
```

## Tips for Success

### Combat Tips
- **Don't waste time** - Keep hitting enemies to build emotion
- **Use space wisely** - Only super attack when you have a good target
- **Keep moving** - Don't get cornered by multiple enemies
- **Watch your health** - The red bar is your life

### Platform Tips
- **Practice jumping** - You can control mid-air, tap jump early/late for height
- **Watch the moving platforms** - Time your jumps to land on them
- **Use height** - Jump up to avoid enemies below you

### Emotion Meter Tips
- **Fill it fast** - Basic attacks give 8 points each
- **Defeating enemies** - Gives 25 points (more efficient!)
- **Super attack resets it** - Back to 0, so use it wisely
- **It's powerful** - 50 damage vs 15 for basic attacks

## Troubleshooting

### "Game won't start"
- Make sure pygame is installed: `pip install pygame==2.5.2`
- Make sure you're in the vegetable_war directory

### "Game runs very slow"
- Close other applications
- Check system CPU usage
- The game should run at 60 FPS

### "No sound"
- Sound uses simple procedural generation
- The game works fine without audio

### "Graphics look weird"
- Try running from a different terminal
- Update your graphics drivers

## File Structure

If you want to explore the code:
```
vegetable_war/
├── onions_may_cry.py      ← Run this to play!
├── run.sh                  ← Or run this
├── requirements.txt        ← Dependencies
├── README.md              ← Full documentation
├── GAMEPLAY.md            ← Detailed gameplay guide
└── src/
    ├── main.py            ← Main game loop
    ├── player.py          ← Your character (onion)
    ├── enemies.py         ← Enemy types (beans, peas, garlic)
    ├── platforms.py       ← Level platforms
    ├── levels.py          ← Level definitions
    ├── story.py           ← Cutscenes and dialogue
    ├── audio.py           ← Sound system
    ├── effects.py         ← Particle effects
    └── constants.py       ← Game settings
```

## What to Expect

### Stage 1
- **Difficulty**: Easy
- **Enemies**: Brown Beans (slow, moderate health)
- **Time**: 2-3 minutes
- **Goal**: Get comfortable with combat and jumping

### Stage 2
- **Difficulty**: Medium
- **Enemies**: Green Peas (fast, low health)
- **Challenge**: Moving platforms + fast enemies
- **Time**: 3-4 minutes

### Stage 3
- **Difficulty**: Hard
- **Enemies**: Giant Garlic Boss (powerful, summons minions)
- **Challenge**: Boss fight + strategy
- **Time**: 5-10 minutes

## Story Overview

You're an **Onion** trying to survive in a garden. Three resources keep you alive:
1. **Nutrients** (from soil)
2. **Sunlight** (from above)
3. **Water** (from rain)

But invaders want these too:
- **Beans** compete for nutrients
- **Peas** compete for sunlight
- **Garlic** competes for water (and leads the invasion)

Only by defeating them all can you protect your garden!

## Advanced Tips (For Replays)

- Try to beat stages without taking damage
- See how many enemies you can hit with one super attack
- Time yourself to find your best speed
- Memorize enemy patterns for perfect dodging
- Use terrain to your advantage

## Need Help?

See the detailed guides:
- **GAMEPLAY.md** - Full gameplay mechanics and strategies
- **README.md** - Technical information and features

Have fun! You may be an onion that may cry, but you will never break! 🧅
