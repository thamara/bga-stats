from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.timezone import make_aware

from .models import PlayerModel, GameModel
from .stats import Stats
from .prettifier import get_pretty_name

from datetime import datetime
import json
import requests

def get_player_name_from_table_info(player_id, game_info):
    players = list(map(int, game_info['players'].split(',')))
    player_names = game_info['player_names'].split(',')
    return player_names[players.index(player_id)]


def process_game(game_info, player):
    # Store this game
    start = make_aware(datetime.utcfromtimestamp(int(game_info['start'])))
    end = make_aware(datetime.utcfromtimestamp(int(game_info['end'])))
    elo_penalty = int(game_info['elo_after']) if 'elo_after' in game_info else 0
    elo_after = int(game_info['elo_after']) if 'elo_after' in game_info else 0
    game = GameModel(player=player,
                     table_id=game_info['table_id'], 
                     game_name=game_info['game_name'],
                     pretty_game_name=get_pretty_name(game_info['game_name']),
                     game_id=game_info['game_id'],
                     start=start,
                     end=end,
                     duration=end -start,
                     normalend=game_info['normalend'],
                     concede=game_info['concede'],
                     unranked=game_info['unranked'],
                     elo_win=game_info['elo_win'],
                     elo_penalty=elo_penalty,
                     elo_after=elo_after,
                     players=game_info['players'],
                     player_names=game_info['player_names'],
                     scores=game_info['scores'],
                     ranks=game_info['ranks'])
    return game

def retrieve_games(email, password, player_id:int, max_pages=100):
    with requests.session() as c:
        url_login = "http://en.boardgamearena.com/account/account/login.html"
        prm_login = {'email': email, 'password': password, 'rememberme': 'on', 'redirect': 'join', 'form_id': 'loginform'}
        # This is here just to validate that user is logged in
        r = c.post(url_login, params = prm_login)
        if r.status_code != 200:
            raise Exception("Could not login. Please check your email and password.")
        
        url = f'https://boardgamearena.com/gamestats/gamestats/getGames.html?player={player_id}'
        params = {'opponent_id': 0, 'finished': 1, 'updateStats': 0, 'page': 1}

         ## Get last known Game id as we stop processing when we hit that
        last_table_in_db = GameModel.objects.all().filter(player=player_id).order_by('-table_id').first()
        player = None
        stop_processing = False
        for page in range(1, max_pages):
            if stop_processing:
                break
            params['page'] = page
            r = c.get(url, params = params)
            if r.status_code != 200:
                break
            
            y = json.loads(r.text)
            results = y['data']['tables']
            if len(results) == 0:
                break
            
            # Save user (if not yet saved), for this, retrieve its name
            # from the player_names array
            if player is None:
                player_name = get_player_name_from_table_info(player_id, results[0])
                player = PlayerModel(id=player_id, name=player_name)
                player.save()
            
            for i in results:
                game = process_game(i, player)
                stop_processing = last_table_in_db is not None and int(game.table_id) == int(last_table_in_db.table_id)
                if stop_processing:
                    print(f'Stop processign as table {game} is in db for this player')
                    break
                game.save()
    
    return GameModel.objects.all().filter(player_id=player_id)

def index(request):
    return render(request, 'index.html')

def user_stats_post(request):
    if request.method == "POST":
        player_id = request.POST.get('player-id')
        return user_stats(request, player_id)

def user_stats(request, player_id):
    print(player_id)
    if request.method == "POST":
        player_id = request.POST.get('player-id') if not player_id else player_id

    try:
        games = retrieve_games('dummy_email', 'dummy_password', int(player_id))
        stats = Stats(games)
        context = {
            'stats': stats,
            'heatmap_data': stats.get_games_by_date(),
        }
        return render(request, 'user_stats.html', context)
    except Exception as e:
        print(f'Got exception {e}')
        raise Http404(e)

def game_detail(request, player_id, game):
    try:
        games = GameModel.objects.all().filter(player_id=player_id, game_name=game)
        context = {
            'games': games,
        }
        return render(request, 'game_detail.html', context)
    except Exception as e:
        print(f'Got exception {e}')
        raise Http404(e)

def table_detail(request, player_id, table):
    try:
        game = GameModel.objects.all().get(player_id=player_id, table_id=table)
        context = {
            'game': game,
        }
        return render(request, 'table_detail.html', context)
    except Exception as e:
        print(f'Got exception {e}')
        raise Http404(e)