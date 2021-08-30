from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import Http404
from .models import Game
from .stats import Stats
import requests
import json

def retrieve_games(email, password, player_id, max_pages=2):
    games = []
    with requests.session() as c:
        url_login = "http://en.boardgamearena.com/account/account/login.html"
        prm_login = {'email': email, 'password': password, 'rememberme': 'on', 'redirect': 'join', 'form_id': 'loginform'}
        # This is here just to validate that user is logged in
        r = c.post(url_login, params = prm_login)
        if r.status_code != 200:
            raise Exception("Could not login. Please check your email and password.")
        
        url = f'https://boardgamearena.com/gamestats/gamestats/getGames.html?player={player_id}'
        params = {'opponent_id': 0, 'finished': 1, 'updateStats': 0, 'page': 1}

        for page in range(1, max_pages):
            params['page'] = page
            r = c.get(url, params = params)
            if r.status_code != 200:
                break
            
            y = json.loads(r.text)
            if len(y["data"]["tables"]) == 0:
                break
            for i in y["data"]["tables"]:
                games.append(Game(i['table_id'], i['game_name'], i['game_id'], i['start'], i['end'], i['players'], i['player_names'], i['scores'], i['ranks']))
    return games

def index(request):
    return render(request, 'index.html')

def user_stats(request):
    if request.method == "POST":
        player_id = request.POST.get('player-id')

        try:
            games = retrieve_games('dummy_email', 'dummy_password', player_id)
            stats = Stats(games)
            context = {
                'stats': stats,
            }
            return render(request, 'user_stats.html', context)
        except Exception as e:
            print(f'Got exception {e}')
            raise Http404(e)
    print('No request POST')
    raise Http404("Something went wrong. :(")