import os
import unittest
import tempfile
import json
from pathlib import Path

from src.leaderboard_server import app, repository
from src.leaderboard_db import LeaderboardRepository
import src.leaderboard_server as server

class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        # temp files for sqlite testing
        self.db_file, self.db_path = tempfile.mkstemp()

        self.test_repository = LeaderboardRepository(db_path=Path(self.db_path))

        self.orginal_repository = server.repository
        server.repository = self.test_repository

        # set flask to testing
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def cleanUp(self):
        server.repository = self.orginal_repository
        os.close(self.db_file)        
        os.unlink(self.db_path)        

    def test_web_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    # Tests for APIs
    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})
    
    def test_submit_and_get_score(self):
        # Test submitting a score
        payload = {"username": "player1", "score": 1200, "completion_time_ms": 85321, "level_name": "level_1"}
        post_reponse = self.client.post('/api/scores', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(post_reponse.status_code, 201)
        
        # Test retrving a score
        get_response = self.client.get('/api/scores')
        data = get_response.get_json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["entries"][0]["username"], "player1")
        self.assertEqual(data["entries"][0]["score"], 1200)
        self.assertEqual(data["entries"][0]["completion_time_ms"], 85321)
        self.assertEqual(data["entries"][0]["level_name"], "level_1")

    def test_validation_rules(self):
        # Test username length
        payload = {"username": "A" * 33, "score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("32 characters", response.get_json()["error"])

        # Test username None
        payload = {"username": None, "score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test username whitespace
        payload = {"username": "   ", "score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test username empty
        payload = {"username": "", "score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test username trim
        payload = {"username": "  player2  ", "score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/scores')
        username = response.get_json()["entries"][0]["username"]
        self.assertEqual(username, "player2")

        # Test username number
        payload = {"username": 10, "score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test negative score
        payload = {"username": "Player", "score": -5, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test non-int score
        payload = {"username": "Player", "score": 5.0, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test string score
        payload = {"username": "Player", "score": "5.0", "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test negative time
        payload = {"username": "Player", "score": 10, "completion_time_ms": -10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test non-int time
        payload = {"username": "Player", "score": 10, "completion_time_ms": 10.0, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test string time
        payload = {"username": "Player", "score": 10, "completion_time_ms": "10", "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test level_name number
        payload = {"username": "Player", "score": 10, "completion_time_ms": 10, "level_name": 10}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test level_name number
        payload = {"username": "Player", "score": 10, "completion_time_ms": 10, "level_name": None}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test level_name whitespace
        payload = {"username": "Player", "score": 10, "completion_time_ms": 10, "level_name": "  "}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test level_name empty
        payload = {"username": "Player", "score": 10, "completion_time_ms": 10, "level_name": ""}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test missing username
        payload = {"score": 10, "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing completion_time_ms
        payload = {"username": "Player", "completion_time_ms": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing score
        payload = {"username": "Player", "score": 10, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing level_name
        payload = {"username": "Player", "score": 10, "completion_time_ms": 10}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test completly empty
        payload = None
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_ranking_order(self):
        # high score, slow time
        payload = {"username": "player1", "score": 100,  "completion_time_ms": 2000, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # same score, faster time should be Rank 1
        payload = {"username": "player2", "score": 100, "completion_time_ms": 1000, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # lower score
        payload = {"username": "player3", "score": 50, "completion_time_ms": 500, "level_name": "level_1"}
        response = self.client.post('/api/scores', json=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/scores')
        entries = response.get_json()["entries"]

        self.assertEqual(entries[0]["username"], "player2")
        self.assertEqual(entries[0]["rank"], 1)
        self.assertEqual(entries[1]["username"], "player1")
        self.assertEqual(entries[1]["rank"], 2)
        self.assertEqual(entries[2]["username"], "player3")
        self.assertEqual(entries[2]["rank"], 3)

    def test_level_filtering(self):
        payload = {"username": "player1", "score": 10, "completion_time_ms": 1, "level_name": "easy"}
        self.client.post('/api/scores', json= payload)
        payload = {"username": "player2", "score": 10, "completion_time_ms": 1, "level_name": "hard"}
        self.client.post('/api/scores', json=payload)

        response = self.client.get('/api/scores?level_name=hard')
        data = response.get_json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["entries"][0]["username"], "player2")
        
        response = self.client.get('/api/scores?level_name=easy')
        data = response.get_json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["entries"][0]["username"], "player1")

    def test_safe_limit(self):
        payload = {"username": "player1", "score": 1200, "completion_time_ms": 85321, "level_name": "level_1"}
        post_reponse = self.client.post('/api/scores', json=payload)
        self.assertEqual(post_reponse.status_code, 201)
        post_reponse = self.client.post('/api/scores', json=payload)
        self.assertEqual(post_reponse.status_code, 201)
        post_reponse = self.client.post('/api/scores', json=payload)
        self.assertEqual(post_reponse.status_code, 201)

        # Test explicit limit
        get_response = self.client.get('/api/scores?limit=2')
        self.assertEqual(len(get_response.get_json()["entries"]), 2)

        # Test cap (asking for more than exists is fine, but verify logic doesn't crash)
        get_response = self.client.get('/api/scores?limit=999')
        self.assertLessEqual(len(get_response.get_json()["entries"]), 200)

    def test_tie_order(self):
        payload = {"username": "player1", "score": 100, "completion_time_ms": 100, "level_name": "level_1"}
        self.client.post('/api/scores', json= payload)
        payload = {"username": "player2", "score": 100, "completion_time_ms": 100, "level_name": "level_1"}
        self.client.post('/api/scores', json=payload)

        response = self.client.get('/api/scores')
        entries = response.get_json()["entries"]
        
        self.assertEqual(entries[0]["username"], "player1")
        self.assertEqual(entries[1]["username"], "player2")

    def test_malformed_json(self):
        payload = '{"username": "broken"'
        response = self.client.post('/api/scores', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON", response.get_json()["error"])
    
    def test_non_json(self):
        payload = "username=player&score=10"
        response = self.client.post('/api/scores', data=payload, content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON", response.get_json()["error"])
    
    def test_api_method(self):
        # PUT method
        response = self.client.put('/api/scores', json={})
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

        # DELETE method
        response = self.client.delete('/api/scores')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
    
if __name__ == "__main__":
    unittest.main()