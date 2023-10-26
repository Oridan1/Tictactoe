import json
from django.test import TestCase
from django.urls import reverse
from .models import Game, Player

class GameModelTest(TestCase):
    def setUp(self):
        # Create a sample player
        self.player1 = Player.objects.create(name="Player 1", symbol="X")
        self.player2 = Player.objects.create(name="Player 2", symbol="O")
        
        # Create a game
        self.game = Game.objects.create(board=[[None, None, None], [None, None, None], [None, None, None]])

    def test_game_creation(self):
        self.assertEqual(self.game.movements_played, 0)
        self.assertEqual(self.game.next_turn, "")
        self.assertIsNone(self.game.winner)

    def test_add_players_to_game(self):
        self.game.players.add(self.player1, self.player2)
        self.assertEqual(self.game.players.count(), 2)

class PlayerModelTest(TestCase):
    def test_player_creation(self):
        player = Player.objects.create(name="Test Player", symbol="X")
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.symbol, "X")

class TicTacToeAPITest(TestCase):
    def setUp(self):
        self.player_data = [
            {"name": "Player1", "symbol": "X"},
            {"name": "Player2", "symbol": "O"},
        ]

    def create_game(self):
        url = reverse("create_game")
        data = {
            "players": self.player_data,
            "starting_player": "Player1",
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        return response

    def test_create_game(self):
        response = self.create_game()
        self.assertEqual(response.status_code, 200)
        self.assertIn("game_id", response.json())
        self.assertEqual(response.json()["movements_played"], 0)
        self.assertEqual(response.json()["next_turn"], "Player1")
        self.assertEqual(len(response.json()["players"]), 2)
        self.assertEqual(response.json()["players"][0]["name"], "Player1")
        self.assertEqual(response.json()["players"][1]["name"], "Player2")
        self.assertEqual(response.json()["players"][0]["symbol"], "X")
        self.assertEqual(response.json()["players"][1]["symbol"], "O")

    def test_submit_move(self):
        response_create_game = self.create_game()
        game_id = response_create_game.json()["game_id"]
        url = reverse("submit_move", args=[game_id])
        data = {
            "player": "Player1",
            "row": 1,
            "column": 2,
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["movements_played"], 1)
        self.assertEqual(response.json()["next_turn"], "Player2")
        self.assertEqual(response.json()["board"][1][2], "X")  # Check if the move is correctly reflected in the board

    def test_list_games(self):
        response_create_game = self.create_game()
        response = self.client.get(reverse("list_games"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["games"]), 1)  # Check if the created game is in the list

    def test_retrieve_game(self):
        response_create_game = self.create_game()
        game_id = response_create_game.json()["game_id"]
        response = self.client.get(reverse("retrieve_game", args=[game_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["game"]["game_id"], game_id)

    def test_delete_game(self):
        response_create_game = self.create_game()
        game_id = response_create_game.json()["game_id"]
        response = self.client.delete(reverse("delete_game", args=[game_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["game_id"], game_id)
