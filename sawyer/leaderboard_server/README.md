# Leaderboard Server - Architectural Spike

Dead simple proof of concept: multiple clients write scores to shared database, viewable on webpage.

## Setup

```bash
pip install flask requests
```

## Run

Terminal 1:
```bash
python server.py
```

Terminal 2:
```bash
python client.py
```

Browser: `http://localhost:5001`

## Multi-device

Find your IP: `hostname -I`

From another device: `python client.py http://YOUR_IP:5001`

## What it does

- Server stores scores in SQLite
- Web page shows scores (auto-refreshes every 3 seconds)
- Client submits player/score/time from any terminal
- Tracks which device submitted each score

That's it.
