# CS518-SWE-Projects

## Build
```
git clone [text](https://github.com/Obada-Salman/CS518-SWE-Projects.git)

# Game was developted on python 3.14
python3.14 -m venv .env

# Activate enviorment os dependent
# linux/macOS
source .env/bin/activate
# windows (powershell)
.env\Scripts\Activate.ps1
# windows (cmd)
venv\Scripts\activate.bat

pip install -r requirements.txt
pip install pyinstaller # pyinstaller for python 3.14 isn't compatiable with pathlib
pyinstaller --name vegtable_wars --onefile --add-data "assets:assets" --add-data "levels/story:levels/story" src/main.py
```

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
