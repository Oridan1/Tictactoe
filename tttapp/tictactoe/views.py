import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Game, Player

@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            players = data.get('players')
            starting_player = data.get('starting_player')

            if len(players) != 2:
                return JsonResponse({'error': 'Games only support 2 players'})
            
            if not starting_player:
                return JsonResponse({'error': 'provide a starting player'})

            game = Game(next_turn=starting_player)
            game.save()

            for _, player_data in enumerate(players):
                player = Player(name=player_data['name'], symbol=player_data['symbol'])
                player.save()
                game.players.add(player)

            game.save()

            response_data = {
                'game_id': game.id,
                'players': [{'name': p.name, 'symbol': p.symbol} for p in game.players.all()],
                'movements_played': 0,
                'next_turn': starting_player,
                'board': [['', '', ''], ['', '', ''], ['', '', '']],
                'winner': None
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def submit_move(request, game_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            player_name = data.get('player')
            row = data.get('row')
            column = data.get('column')

            game = Game.objects.get(pk=game_id)

            if game.winner:
                return JsonResponse({'error': 'The game has already ended'})

            if player_name != game.next_turn:
                return JsonResponse({'error': 'Not your turn'})

            if game.board[row][column]:
                return JsonResponse({'error': 'Invalid move'})

            player = game.players.get(name=player_name)

            game.board[row][column] = player.symbol
            game.movements_played += 1
            game.next_turn = player_name if game.next_turn != player_name else game.players.exclude(name=player_name).first().name

            game.winner = check_winner(game.board)
            if not game.winner and game.movements_played == 9:
                game.winner = "Tie"

            game.save()

            response_data = {
                'game_id': game.id,
                'players': [{'name': p.name, 'symbol': p.symbol} for p in game.players.all()],
                'movements_played': game.movements_played,
                'next_turn': game.next_turn,
                'board': game.board,
                'winner': game.winner
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})


def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0]:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col]:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]

    return None


def list_games(request):
    games = Game.objects.all()
    game_list = []
    
    for game in games:
        game_info = parse_game_to_json(game)        
        game_list.append(game_info)

    return JsonResponse({'games': game_list})


def parse_game_to_json(game):
    return {
            'game_id': game.id,
            'players': [{'name': player.name, 'symbol': player.symbol} for player in game.players.all()],
            'movements_played': game.movements_played,
            'next_turn': game.next_turn,
            'board': game.board,
            'winner': game.winner
        }


def retrieve_game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        game_info = parse_game_to_json(game)        
        return JsonResponse({'game': game_info})

    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'})


@csrf_exempt
def delete_game(request, game_id):
    if request.method == 'DELETE':
        try:
            game = Game.objects.get(pk=game_id)
            game.delete()
            
            return JsonResponse({'game_id': game_id})
        
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'})
    
    return JsonResponse({'error': 'Invalid request method'})
