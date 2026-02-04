import requests
import socket
import sys

server = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'
device = socket.gethostname()

player = input("Player name: ")
score = int(input("Score: "))
time = float(input("Time (seconds): "))

data = {'player': player, 'score': score, 'time': time, 'device': device}
response = requests.post(f'{server}/submit', json=data)

print("Submitted!" if response.ok else "Failed!")
