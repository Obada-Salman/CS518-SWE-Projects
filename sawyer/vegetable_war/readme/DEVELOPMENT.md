# Development Guide - Onions May Cry

This guide explains the code structure and how to add new features.

## Project Structure

```
vegetable_war/
├── src/
│   ├── main.py           # Game class, main loop, state machine
│   ├── constants.py      # All game constants (easy to tweak)
│   ├── player.py         # Player class (onion)
│   ├── enemies.py        # Enemy classes (Bean, Pea, Garlic, Boss)
│   ├── platforms.py      # Platform classes
│   ├── levels.py         # Level class with level definitions
│   ├── story.py          # Cutscene and dialogue system
│   ├── audio.py          # Sound effects manager
│   └── effects.py        # Visual effects (particles, shake, text)
├── assets/
│   ├── sprites/          # Sprite images (currently unused - procedural)
│   ├── sounds/           # Audio files (currently unused - procedural)
│   └── fonts/            # Font files (currently unused)
└── [configuration files]
```

## Key Components

### 1. Game Class (main.py)
The main game controller. Manages:
- Game state (menu, playing, cutscene, game over)
- Level progression
- Collision detection
- Effect updates
- UI drawing

**State Machine:**
```
MENU → CUTSCENE → PLAYING ←→ CUTSCENE ← GAME_OVER
                ↓
          LEVEL_COMPLETE
```

### 2. Player Class (player.py)
The onion character. Features:
- Position and velocity (platformer physics)
- Health system with invincibility frames
- Emotion meter
- Attack detection and super attacks
- Sprite rendering with dynamic layers

**Key Methods:**
- `handle_input()` - Process keyboard
- `update()` - Physics and state
- `take_damage()` - Health management
- `super_attack()` - Special ability
- `get_attack_hitbox()` - Combat detection

### 3. Enemy System (enemies.py)

#### Enemy Class
Generic enemy with:
- AI behavior (patrol, attack range)
- Health and damage
- Attack cooldown
- Type-specific stats (Bean, Pea, Garlic)

#### Boss Class
Extends Enemy with:
- Phase system
- Summon ability
- Larger stats
- Special patterns

**Enemy Types:**
- **Bean**: Slow, moderate health (30), damage 10
- **Pea**: Fast, low health (20), damage 8
- **Garlic**: Slow, high health (40), damage 15
- **Boss**: Very high health (150), damage 20

### 4. Platform System (platforms.py)
Three platform types:
- **Platform**: Static ground
- **MovingPlatform**: Oscillates between two points
- **BreakablePlatform**: Can be destroyed (expandable)

### 5. Level System (levels.py)
Each level defines:
- Platform layout
- Enemy placement
- Boss (if applicable)
- Story/setting
- Resource requirements

**Levels 1-3 are hardcoded** - extend with more levels here.

### 6. Story System (story.py)
Manages cutscenes:
- **Cutscene**: Displays dialogue, typed text, continues with SPACE
- **StoryManager**: Holds all cutscenes, plays them when triggered

### 7. Effects System (effects.py)
Visual feedback:
- **Particle**: Individual particle with physics
- **ParticleSystem**: Manages all particles
- **ScreenShake**: Camera shake on impact
- **FloatingText**: Damage/score numbers
- **FloatingTextManager**: Manages floating text

## How to Add Features

### Adding a New Enemy Type

1. **In enemies.py**, modify the Enemy `__init__`:
```python
elif enemy_type == "new_enemy":
    self.health = 35
    self.max_health = 35
    self.damage = 12
    self.speed = 3
    self.color = (100, 50, 200)
    self.accent = (150, 100, 255)
```

2. **In levels.py**, add it to level spawning:
```python
self.enemies.add(Enemy(x, y, "new_enemy"))
```

3. **Test** - Run the game and fight it!

### Adding a New Level

1. **In levels.py**, add a new level method:
```python
def _create_level_4(self):
    """Level 4: New content"""
    self.story = "New level description"
    self.background_color = (100, 100, 200)
    
    # Add platforms
    self.platforms.add(Platform(0, 600, 200, 100))
    self.platforms.add(MovingPlatform(300, 400, 150, 50, 300, 700, 2))
    
    # Add enemies
    self.enemies.add(Enemy(400, 400, "bean"))
    self.enemies.add(Boss(600, 200, "giant_garlic"))
    
    # Set resources needed
    self.resources_needed = {NUTRIENTS: 5, SUNLIGHT: 5, WATER: 5}
```

2. **In story.py**, add intro and outro cutscenes:
```python
self.cutscenes["level4_intro"] = Cutscene([
    "Stage 4: New challenge",
    "Face the ultimate test..."
])
```

3. **In main.py**, add to the level progression:
```python
cutscene_keys = {
    1: "level1_intro",
    2: "level2_intro",
    3: "level3_intro",
    4: "level4_intro",  # Add this
}
```

### Tweaking Game Balance

All tunable constants are in `constants.py`:

```python
# Physics
GRAVITY = 0.6           # How fast things fall
JUMP_STRENGTH = -15     # How high you jump
MOVE_SPEED = 5          # How fast you move

# Combat
PLAYER_MAX_HEALTH = 100
EMOTION_METER_MAX = 100
EMOTION_GAIN_ON_HIT = 8
EMOTION_GAIN_ON_KILL = 25
SUPER_ATTACK_DAMAGE = 50
SUPER_ATTACK_COOLDOWN = 120

# Screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
```

Change any values to balance the game!

### Adding Visual Effects

Use the **ParticleSystem** in main.py:

```python
# On hit
self.particle_system.emit_hit(x, y, count=8, color=YELLOW)

# On super attack
self.particle_system.emit_super_effect(x, y)

# Screen shake
self.screen_shake.start()

# Floating text
self.floating_text.add_text(x, y, "CRITICAL HIT!", RED)
```

### Adding Sound Effects

The **SoundManager** is in audio.py. Currently procedural but expandable:

```python
# Play existing sound
self.sound_manager.play_sound('hit')

# Add new sound
self.sound_manager.sounds['new_sound'] = create_your_sound()
self.sound_manager.play_sound('new_sound')
```

To add actual audio files:
1. Place .wav files in `assets/sounds/`
2. Load them in `audio.py`:
```python
self.sounds['attack'] = pygame.mixer.Sound('assets/sounds/attack.wav')
```

## Architecture Patterns

### State Machine (main.py)
Uses `self.state` to manage game flow:
```python
if self.state == STATE_PLAYING:
    # Update game
elif self.state == STATE_CUTSCENE:
    # Show story
elif self.state == STATE_MENU:
    # Show menu
```

### Sprite Groups (pygame)
Uses pygame sprite groups for efficient rendering:
```python
self.enemies = pygame.sprite.Group()
self.platforms = pygame.sprite.Group()
```

### Component-Based Design
Each entity (Player, Enemy) is self-contained with:
- Rendering (`create_sprite()`)
- Physics (`update()`)
- Collision (`take_damage()`)
- Input (`handle_input()`)

## Testing & Debugging

### Debug Features Already in Code
- Invincibility frames (flash effect)
- Attack hitbox display (yellow outline)
- Enemy health bars
- Resource counter
- Emotion meter visualization

### To Add More Debugging
Edit `main.py` draw section:
```python
# Draw collision rectangles
pygame.draw.rect(self.screen, BLUE, enemy.rect, 2)

# Print variable values
print(f"Player health: {self.player.health}")

# Visual indicators
pygame.draw.circle(self.screen, RED, (x, y), 5)
```

## Performance Optimization

Current bottlenecks to watch:
1. **Particle rendering** - Limit max particles
2. **Collision detection** - O(n²) with enemies
3. **Sprite creation** - Don't recreate every frame

### Optimization Ideas
- Use sprite batching
- Implement object pooling for particles
- Cache sprite images instead of recreating
- Use quad trees for collision detection
- Profile with `cProfile` module

## Future Enhancement Ideas

### Easy (1-2 hours)
- [ ] Additional enemy types
- [ ] More levels
- [ ] Sound effects (wav files)
- [ ] Settings menu (volume, difficulty)
- [ ] Pause feature

### Medium (4-8 hours)
- [ ] Custom sprite artwork
- [ ] Animated sprites
- [ ] Power-ups and items
- [ ] Difficulty modes
- [ ] High score system

### Hard (8+ hours)
- [ ] Procedural level generation
- [ ] Save/load system
- [ ] Multiplayer mode
- [ ] Custom map editor
- [ ] Advanced AI behaviors
- [ ] Particle shader system

## Code Style

The codebase follows:
- **PEP 8** - Python style guide
- **Clear naming** - `player_health` not `ph`
- **Comments** - For complex logic
- **Type hints** - Where helpful (optional)

## Common Issues & Solutions

### "Player doesn't respond to input"
Check `handle_input()` is called in main loop

### "Enemies not spawning"
Check level `_create_level_X()` adds to `self.enemies`

### "Collision not working"
Verify `update()` is called for all entities

### "Game crashes on boss"
Boss spawning might fail - check level setup

## Resources

- **Pygame Docs**: https://www.pygame.org/docs/
- **Game Dev Patterns**: https://gameprogrammingpatterns.com/
- **Python Tips**: https://pep8.org/

## Contributing

To improve the game:
1. Make a change in `src/`
2. Test it thoroughly
3. Update this guide if adding features
4. Keep code clean and documented

---

Happy developing! 🧅🎮
