from flask import Flask, request, jsonify
import sqlite3
import socket

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('scores.db')
    conn.execute('CREATE TABLE IF NOT EXISTS scores (player TEXT, score INT, time REAL, device TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('scores.db')
    rows = conn.execute('SELECT player, score, time, device FROM scores ORDER BY score DESC').fetchall()
    conn.close()
    
    html = '<h1>Leaderboard</h1><table border=1><tr><th>Player</th><th>Score</th><th>Time</th><th>Device</th></tr>'
    for row in rows:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]:.1f}s</td><td>{row[3]}</td></tr>'
    html += '</table><script>setTimeout(()=>location.reload(),3000)</script>'
    return html

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    conn = sqlite3.connect('scores.db')
    conn.execute('INSERT INTO scores VALUES (?,?,?,?)', 
                 (data['player'], data['score'], data['time'], data['device']))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

if __name__ == '__main__':
    init_db()
    print(f"Server running at http://localhost:8080")
    app.run(host='0.0.0.0', port=8080)
