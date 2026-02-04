# Onions May Cry - Gameplay Guide

## Quick Start

```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war
python3 onions_may_cry.py
```

## Game Objective

Defend your garden from three waves of vegetable invaders:
1. **Beans** - Compete for nutrients
2. **Peas** - Compete for sunlight  
3. **Garlic** - Led by a mighty General (final boss)

Each enemy type has different stats, speeds, and behaviors. Learn their patterns to defeat them!

## Controls

| Input | Action |
|-------|--------|
| **A** | Move left |
| **D** | Move right |
| **W** | Jump |
| **SPACE** | Basic Attack (15 damage) |
| **SHIFT** | Super Attack (50 damage, requires full emotion meter) |
| **ESC** | Quit |

## Combat System

### Health & Defense
- You start with **100 HP**
- Each hit damages you based on enemy damage value
- You have visual **layers** - watch them shed as you take damage
- Taking damage puts you in **invincibility frames** temporarily

### Emotion Meter
The **Emotion Meter** (purple bar) is your key to victory:
- Fills by **8 points** each time you hit an enemy
- Fills by **25 points** when you defeat an enemy
- Maxes out at **100 points**
- When full, you can use your **SUPER ATTACK**
- Using super attack resets the meter to 0

### Attack Strategy
1. **Build Emotion**: Land basic attacks to fill emotion meter
2. **Save Energy**: Don't rush - patience builds powerful attacks
3. **Super Attack**: When meter is full and opportunity arises, unleash it
4. **Combo**: Mix basic attacks with dodging enemy patterns

## Enemy Types

### Bean 🟤
- **Health**: 30 HP
- **Damage**: 10
- **Speed**: Slow (2 units/sec)
- **Behavior**: Patrols slowly, attacks in range
- **Strategy**: Easy target, use for building emotion meter

### Pea 🟢
- **Health**: 20 HP
- **Damage**: 8
- **Speed**: Fast (4 units/sec)
- **Behavior**: Quick patrols, hard to hit
- **Strategy**: Use moving platforms to chase, or wait for it to approach

### Garlic ⚪
- **Health**: 40 HP
- **Damage**: 15
- **Speed**: Slow (2 units/sec)
- **Behavior**: Deals high damage, worth avoiding
- **Strategy**: Keep distance, strike when safe

### Giant Garlic General (Boss) 👑
- **Health**: 150 HP
- **Damage**: 20
- **Size**: Larger hitbox
- **Special**: Summons Bean minions as you fight
- **Strategy**: 
  - Focus emotion meter early
  - Build up super attacks to burst damage
  - Deal with summoned beans quickly
  - Watch for patterns - boss has phases

## Levels

### Stage 1: The Bean Invasion
- **Enemies**: Multiple Beans
- **Terrain**: Simple platforms at varying heights
- **Difficulty**: Beginner-friendly
- **Objective**: Defeat all Beans
- **Resources Needed**: 5 Nutrients

### Stage 2: The Pea Swarm
- **Enemies**: Multiple Peas (fast!)
- **Terrain**: Moving platforms that shift side-to-side
- **Difficulty**: Intermediate - requires timing
- **Objective**: Navigate platforms and defeat Peas
- **Resources Needed**: 5 Sunlight

### Stage 3: The Garlic Conspiracy
- **Enemies**: Giant Garlic General + Beans
- **Terrain**: Simple arena platforms
- **Difficulty**: Hard - boss fight
- **Objective**: Defeat the Giant Garlic General
- **Resources Needed**: 5 Water

## Platform Types

### Normal Platform (Brown)
- Standard solid platform
- Never moves
- Safe to stand on indefinitely

### Moving Platform (Gray)
- Moves back and forth
- Time your jumps to land on them
- Useful for reaching high areas

### Water Platform (Blue)
- (Future feature) May have special properties
- Currently same as normal platforms

## Winning Strategies

### For Beans (Level 1)
1. Jump to higher platforms to avoid other beans
2. Use basic attacks repeatedly to build emotion
3. When emotion is full, find a bean and use super attack
4. Defeat remaining beans with basic attacks

### For Peas (Level 2)
1. Use moving platforms to stay in the fight
2. Time your jumps as platforms move
3. Peas are fast - keep your distance initially
4. Build emotion by landing hits
5. Use super attack when you see a good opportunity

### For Boss (Level 3)
1. **Early Phase**: Build emotion meter fast with basic attacks
2. **Mid Phase**: Use super attacks when boss is vulnerable
3. **Late Phase**: Boss gets faster and summons more minions
4. **Key**: Don't get greedy - take safe hits
5. **Finisher**: Use your last super attack to finish it off

## Resource System

Throughout each level, you collect resources as you defeat enemies:
- **Nutrients** (1 per basic kill, 2 per super kill)
- **Sunlight** (earned from Peas primarily)
- **Water** (earned from defeating boss)

These track your progress but also tell the story - you're consuming what your enemies wanted!

## Tips & Tricks

### Pro Tips
1. **Jump height varies**: Hold W longer for higher jumps
2. **Momentum**: You maintain velocity while attacking
3. **Knockback strategy**: Use it to push enemies toward hazards
4. **Super attack timing**: Use it to finish wounded enemies or clear multiple enemies at once
5. **Emotions**: The game literally makes you stronger when emotional - embrace the feels!

### Recovery
- If low on health, stay near platforms
- Avoid unnecessary risks when building emotion
- The invincibility frames give you time to escape

### Audio
- The game has sound effects for:
  - Attacks hitting enemies
  - Super attack charging
  - Enemies defeated
  - Level completion
  - (Procedurally generated - simple beeps for now)

## Game Over Conditions

You lose if:
- Your health reaches 0
- You fall off the bottom of the screen
- The boss (stage 3) defeats all your health

## Victory Conditions

Each level is complete when:
- All enemies are defeated

After all 3 levels, you win the game!

## Story Summary

**The Setup**: You're an onion. Your existence depends on three things:
1. **Nutrients** from the soil
2. **Sunlight** from above
3. **Water** from below

**The Conflict**: Beans, peas, and garlic also need these resources. They've invaded to take what you need to survive.

**The Journey**:
- Stage 1: Face the Bean army
- Stage 2: Outmaneuver the swift Peas
- Stage 3: Confront the Garlic General in an epic final battle

**The Theme**: In defending what you need, you discover an inner emotional strength. Your layers may be shed, but your spirit remains unbroken.

## Replay & Difficulty

### Mastery Goals
- Clear stage 1 without taking damage
- Clear stage 2 without falling off a platform
- Defeat the boss using only 2-3 super attacks
- Collect all possible resources in a single run

### Challenge Ideas
- Try to beat each level with minimal emotion meter usage
- See how fast you can complete all 3 stages
- Memorize enemy patrol patterns for perfect dodging
- Use only super attacks (no basic attacks) for fun

## Technical Info

**Game Engine**: Pygame 2.5.2
**Python Version**: 3.7+
**Screen Resolution**: 1200x700 (60 FPS)
**Save System**: None (no save between sessions)

## Troubleshooting

**Game Won't Start**
- Ensure pygame is installed: `pip install pygame==2.5.2`
- Run from the vegetable_war directory

**Graphics Glitchy**
- Try updating your GPU drivers
- Run in windowed mode (already default)

**No Sound**
- Sound uses procedural generation - some systems may have issues
- The game works fine without audio

**Game Runs Slow**
- Close other applications
- Reduce screen resolution (edit SCREEN_WIDTH/HEIGHT in constants.py)
- Disable sound in audio.py if needed

## Future Features

- Custom sprite artwork
- Animated characters
- Additional levels
- Power-ups and items
- Different difficulty modes
- High score/leaderboard
- Controller support

---

**Remember**: You are an ONION THAT MAY CRY, but one that will never break! 🧅
