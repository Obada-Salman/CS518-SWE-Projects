# Installation Guide - Onions May Cry

## System Requirements

- **OS**: Linux, macOS, or Windows
- **Python**: 3.7 or higher
- **Disk Space**: ~50 MB
- **RAM**: 512 MB minimum (2GB recommended)
- **GPU**: Any modern GPU (integrated is fine)
- **Display**: 1200x700 or larger

## Step-by-Step Installation

### 1. Verify Python Installation

Open a terminal and check your Python version:

```bash
python3 --version
```

You should see `Python 3.7.x` or higher. If not, [install Python 3](https://www.python.org/downloads/).

### 2. Navigate to Game Directory

```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war
```

### 3. Install Dependencies

Install pygame and numpy:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pygame==2.5.2 numpy==1.24.3
```

**Troubleshooting:**
- If `pip` is not found, try `pip3`
- On Linux, you might need: `sudo apt-get install python3-pip`
- On macOS with M1/M2, you might need: `pip install pygame==2.5.2 --prefer-binary`

### 4. Verify Installation

Test that everything imported correctly:

```bash
python3 test_imports.py
```

You should see:
```
Testing game component imports...
  - Importing constants... ✓
  - Importing platforms... ✓
  - Importing enemies... ✓
  - Importing player... ✓
  - Importing levels... ✓
  - Importing story... ✓
  - Importing audio... ✓
  - Importing effects... ✓

✓ All components imported successfully!
```

If you see any errors, go to **Troubleshooting** below.

## Running the Game

### Method 1: Python Command (Recommended)

```bash
python3 onions_may_cry.py
```

### Method 2: Shell Script

```bash
chmod +x run.sh
./run.sh
```

### Method 3: Direct Source

```bash
cd src
python3 main.py
```

## Troubleshooting

### "pygame module not found"

**Problem**: Game won't start saying pygame is missing

**Solution**:
```bash
pip3 install pygame==2.5.2
```

If that doesn't work:
```bash
python3 -m pip install pygame==2.5.2
```

### "python3: command not found"

**Problem**: Python isn't installed or not in PATH

**Solution**:
1. [Install Python 3](https://www.python.org/downloads/)
2. Add Python to PATH if needed
3. Try `python` instead of `python3` (Windows)

### "Permission denied" when running run.sh

**Problem**: Can't execute the shell script

**Solution**:
```bash
chmod +x run.sh
./run.sh
```

### Game runs very slowly

**Problem**: FPS below 60

**Solutions**:
1. Close other applications
2. Update graphics drivers
3. Try `export SDL_VIDEODRIVER=windowed` before running
4. Check CPU/memory usage with `top` or Task Manager

### "No module named 'numpy'"

**Problem**: numpy is missing

**Solution**:
```bash
pip install numpy==1.24.3
```

### Game won't open a window

**Problem**: Nothing appears when running

**Solutions**:
1. Check terminal for error messages
2. Try different terminal emulator
3. Set environment variables:
   ```bash
   export SDL_VIDEODRIVER=x11
   python3 onions_may_cry.py
   ```
4. On WSL (Windows Subsystem for Linux), ensure X11 forwarding is set up

### "Library not found" on macOS

**Problem**: Missing SDL dependencies

**Solution**:
```bash
# Install with Homebrew
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame==2.5.2 --prefer-binary
```

### "pygame module is read-only"

**Problem**: Permission error during installation

**Solution**:
```bash
pip install --user pygame==2.5.2
```

### Game crashes immediately

**Problem**: Crashes on startup with error

**Solutions**:
1. Check error message in terminal
2. Verify all files are present in `src/` directory
3. Try: `python3 -m src.main`
4. Check for Python syntax errors:
   ```bash
   python3 -m py_compile src/*.py
   ```

### No sound/audio issues

**Problem**: No sound effects during gameplay

**Note**: This is normal. The game uses procedural audio generation which may not work on all systems. The game is fully playable without sound.

**Solution**: The game works fine without audio - no action needed.

## Uninstall

To completely remove the game:

```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects
rm -rf vegetable_war
```

To just remove Python dependencies:

```bash
pip uninstall pygame numpy
```

## Advanced Setup

### Virtual Environment (Recommended for Development)

Create isolated Python environment:

```bash
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run game
python3 onions_may_cry.py
```

### Linux (Ubuntu/Debian)

Full setup for fresh Linux install:

```bash
# Install Python and pip
sudo apt-get update
sudo apt-get install python3 python3-pip

# Install pygame system dependencies
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev

# Navigate to game
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war

# Install Python packages
pip3 install -r requirements.txt

# Run game
python3 onions_may_cry.py
```

### macOS

Setup for macOS:

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python (if needed)
brew install python3

# Install SDL dependencies
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

# Navigate to game
cd /home/sawda/CS518/CS-371-518-Software-Engineering-Projects/vegetable_war

# Install dependencies
pip3 install -r requirements.txt --prefer-binary

# Run game
python3 onions_may_cry.py
```

### Windows

Setup for Windows:

1. Install [Python 3](https://www.python.org/downloads/)
   - **Important**: Check "Add Python to PATH" during installation

2. Open Command Prompt and navigate:
   ```cmd
   cd C:\path\to\vegetable_war
   ```

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

4. Run game:
   ```cmd
   python onions_may_cry.py
   ```

## Verify Game Works

### Quick Test

Run this to verify everything is set up:

```bash
python3 test_imports.py
```

Expected output: All components imported successfully ✓

### Full Test

To fully verify the game (may take a moment):

```bash
# Test all imports
python3 test_imports.py

# List game files
ls -la src/

# Check Python syntax
python3 -m py_compile src/*.py
```

## Next Steps

Once installed and working:

1. **Read** [QUICKSTART.md](QUICKSTART.md) - How to play
2. **Play** the game - Run `python3 onions_may_cry.py`
3. **Explore** [GAMEPLAY.md](GAMEPLAY.md) - Strategy guide
4. **Code** [DEVELOPMENT.md](DEVELOPMENT.md) - How to modify

## Getting Help

### Common Resources

1. **Pygame Docs**: https://www.pygame.org/docs/
2. **Python Docs**: https://docs.python.org/3/
3. **Game Files**: Check [INDEX.md](INDEX.md) for directory structure

### Debug Information to Include

If reporting issues, include:
- Python version: `python3 --version`
- Pygame version: `pip show pygame`
- Operating system: `uname -a` (Linux) or `systeminfo` (Windows)
- Error message from terminal
- Steps to reproduce

## Success Indicators

✅ You've successfully installed if:
- `test_imports.py` shows all imports successful
- No error messages appear
- Game window opens when you run it
- You can move, jump, and attack

## Performance Checklist

For optimal performance:
- [ ] Close other applications
- [ ] Ensure good ventilation for laptop
- [ ] Update graphics drivers
- [ ] Verify FPS counter shows ~60 FPS
- [ ] No lag when attacking enemies

---

**Congratulations!** You're ready to play Onions May Cry! 🧅

For next steps, see [QUICKSTART.md](QUICKSTART.md)
