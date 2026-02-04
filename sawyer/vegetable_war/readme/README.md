# Onions May Cry - The Vegetable War

A 2D platformer/fighting game where you play as an onion defending your garden from vegetable invaders.

## Game Overview

You are an **Onion**, guardian of the garden soil. For generations, your kind has thrived, absorbing nutrients, water, and sunlight. But now, Beans, Peas, and Garlic seek to overtake your territory and consume all the garden has to offer!

You must stand against them. Only your emotions will give you strength. The more you fight, the more emotional you become. And when your emotion reaches its peak, unleash your most powerful attack!

## Features

- **Dynamic Combat System**: Attack enemies with spacebar, build up emotion meter for powerful super attacks
- **3 Enemy Types**: Beans, Peas, and Garlic - each with unique behavior and difficulty
- **Boss Fights**: Face mighty vegetable commanders in intense battles
- **Layered Onion Mechanic**: Watch your onion shed layers as you take damage
- **Emotion Meter**: Fills as you deal damage, enables devastating super attacks
- **Story Cutscenes**: Rich narrative with intro, level interludes, and endings
- **Progressive Difficulty**: Three challenging stages with increasing complexity
- **Resource Management**: Collect nutrients, water, and sunlight as you defeat enemies

## Controls

| Key | Action |
|-----|--------|
| **A / D** | Move left / right |
| **W** | Jump |
| **SPACE** | Basic Attack |
| **SHIFT** | Super Attack (when emotion meter is full) |
| **ESC** | Quit Game |

## Game Mechanics

### Combat
- **Basic Attack**: Deal 15 damage to nearby enemies
- **Super Attack**: Deal 50 damage in a large area when emotion meter is full
- **Knockback**: Successful hits push enemies away

### Emotion Meter
- Fills with 8 points per basic hit
- Fills with 25 points per enemy defeated
- Resets when using super attack
- Maximum 100 points

### Enemy Types

1. **Bean** (Brown)
   - Health: 30
   - Damage: 10
   - Speed: Slow
   - Competes for nutrients

2. **Pea** (Green)
   - Health: 20
   - Damage: 8
   - Speed: Fast
   - Competes for sunlight

3. **Garlic** (White)
   - Health: 40
   - Damage: 15
   - Speed: Slow
   - Competes for water

### Story Arc

**Stage 1: The Bean Invasion**
Defeat the bean forces competing for nutrients.

**Stage 2: The Pea Swarm**
Navigate moving platforms and defeat fast-moving peas.

**Stage 3: The Garlic Conspiracy**
Face the Giant Garlic General in an epic final battle!

## Installation & Running

### Requirements
- Python 3.7+
- pygame 2.5.2

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
cd src
python main.py
```

Or use the provided script:
```bash
chmod +x run.sh
./run.sh
```

## File Structure

```
vegetable_war/
├── src/
│   ├── main.py          # Main game loop
│   ├── constants.py     # Game constants
│   ├── player.py        # Player (onion) class
│   ├── enemies.py       # Enemy classes
│   ├── platforms.py     # Platform classes
│   ├── levels.py        # Level definitions
│   ├── story.py         # Story and cutscenes
│   └── audio.py         # Sound system
├── assets/
│   ├── sprites/         # Sprite assets (expandable)
│   ├── sounds/          # Audio files (expandable)
│   └── fonts/           # Font files (expandable)
├── requirements.txt
└── README.md
```

## Future Enhancements

- Custom sprite artwork
- Animated sprites and particles
- Background music and sound effects
- Additional levels and bosses
- Power-ups and items
- Difficulty settings
- High score system
- Pause menu

## Themes

This game explores themes of:
- **Resource Competition**: Different vegetables compete for the same resources
- **Emotional Strength**: The power of emotions in overcoming adversity
- **Sacrifice and Resilience**: Shedding layers but never breaking
- **Environmental Conflict**: The natural competition in a garden ecosystem

## Credits

Made with Pygame. Inspired by Cuphead's combat style and classic platformer games.

---

**Remember**: You may shed layers, but your spirit remains strong. You are an **ONION THAT MAY CRY**, but one that will never break!
