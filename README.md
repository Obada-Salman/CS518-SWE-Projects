# CS518-SWE-Projects

## Build

### Setup
Build Requires python 3.12  
Python 3.12 download site https://www.python.org/downloads/release/python-3120/

### Game

#### Linux and Mac
```
git clone https://github.com/Obada-Salman/CS518-SWE-Projects.git
cd CS518-SWE-Projects

python3.12 -m venv .env
source .env/bin/activate

pip install -r requirements.txt

pyinstaller --name vegtable_wars --onefile --add-data "assets:assets" --add-data "levels/story:levels/story" src/main.py
```

#### Window
```
git clone https://github.com/Obada-Salman/CS518-SWE-Projects.git
cd CS518-SWE-Projects

py -3.12 -m venv .env
.\.env\Scripts\activate

pip install -r requirements.txt

pyinstaller --name vegtable_wars --onefile --add-data "assets:assets" --add-data "levels/story:levels/story" src/main.py

```
### Leaderboard
```
pyinstaller --onefile --name leaderboard_server --add-data "src/templates:templates" src/leaderboard_server.py
```

## Run

### Game

#### Linux and Max
```./dist/vegtable_wars```

#### Window
```./dist/vegtable_wars.exe```

### Leaderboard
#### Linux and Max
```./dist/leaderboard_server```

#### Window
```./dist/leaderboard_server.exe```

Executables can be moved to differnt locations and still run

## Leaderboard scaffold (online + persistent)

This project now includes a minimal online leaderboard backend using Flask + SQLite.

### Files added
- `src/leaderboard_server.py` - Web server + API routes
- `src/leaderboard_db.py` - SQLite persistence layer
- `src/leaderboard_client.py` - Helper function for game-side score uploads
- `src/templates/leaderboard.html` - Simple leaderboard webpage
- `requirements.txt` - Python dependency list

### Install
```bash
pip install -r requirements.txt
```

### Run leaderboard server
```bash
python src/leaderboard_server.py
```

Then open:
- `http://127.0.0.1:5000/` (web leaderboard)
- `http://127.0.0.1:5000/api/health`

SQLite database is created automatically at `data/leaderboard.db`.

### API (for game integration)

Submit a score:
```bash
curl -X POST http://127.0.0.1:5000/api/scores \
	-H "Content-Type: application/json" \
	-d '{
		"username": "player1",
		"score": 1200,
		"completion_time_ms": 85321,
		"level_name": "story_1"
	}'
```

Fetch top scores:
```bash
curl "http://127.0.0.1:5000/api/scores?limit=25"
```

### Tests

Run sprite-focused tests:
```bash
python -m unittest tests/test_sprites.py
```

Run leader-board tests:
```bash
python -m unittest tests/test_leaderboard.py
```

Run all unittest tests:
```bash
python -m unittest discover -s tests
```

## Save Data

The game stores progress in per-slot JSON files.

### Save directory by platform
- Linux/WSL: `~/.local/share/vegtable_wars/saves` (or `$XDG_DATA_HOME/vegtable_wars/saves` when set)
- macOS: `~/Library/Application Support/vegtable_wars/saves`
- Windows: `%LOCALAPPDATA%/vegtable_wars/saves` (fallback: `~/AppData/Local/vegtable_wars/saves`)

### Save slot files
- `slot_1.json`
- `slot_2.json`
- `slot_3.json`

### What is saved
- Player username
- Max unlocked story level
- Current story level
- Resource totals (`water`, `sunlight`, `nutrients`)
- Last updated timestamp (`updated_at`)

Saves are written automatically during gameplay updates and on game quit.
