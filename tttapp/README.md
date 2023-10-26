create a virtual enviroment and then run pip install requirements.txt

to launch the server, run python tttapp/manage.py runserver

to test each end point, use insomnia, o postman with the following requests:

POST
http://127.0.0.1:8000/tictactoe/create-game/

Body:

{
  "players": [
    { "name": "Player1", "symbol": "D" },
    { "name": "Player2", "symbol": "L" }
  ],
  "starting_player": "Player1"
}

POST
http://127.0.0.1:8000/tictactoe/submit-move/<ID>/

Body:
{
  "player": "Player1",
  "row": 0,
  "column": 0
}

GET
http://127.0.0.1:8000/tictactoe/list-games

GET
http://127.0.0.1:8000/tictactoe/retrieve-game/<ID>

DELETE
http://127.0.0.1:8000/tictactoe/delete-game/<ID>/



To run automatic tests:
python tttapp/manage.py test tictactoe
