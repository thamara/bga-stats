from django.db import models
import datetime

from .prettifier import get_pretty_name

from django.db import models

class GameModel(models.Model):
    id = models.IntegerField(primary_key=True)
    game_name = models.CharField(max_length=300)
    pretty_game_name = models.CharField(max_length=300)
    game_id = models.IntegerField(default=0)
    
    start = models.DateTimeField()
    end = models.DateTimeField()
    duration = models.DurationField()

    normalend = models.BooleanField(default=True)
    concede = models.BooleanField(default=False)
    unranked = models.BooleanField(default=False)
    
    elo_win = models.IntegerField(default=0)
    elo_penalty = models.IntegerField(default=0)
    elo_after = models.IntegerField(default=0)
    
    # TODO: should be an array
    players = models.CharField(max_length=500)
    player_names = models.CharField(max_length=500)
    scores = models.CharField(max_length=500)
    ranks = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.pretty_game_name} ({self.id})' 

class PlayerDetailsModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name} ({self.id})' 

class GamesByPlayerModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    # player_id = models.IntegerField(default=0)
    player = models.ForeignKey(PlayerDetailsModel, on_delete=models.CASCADE, default=None)
    game = models.ForeignKey(GameModel, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.player.name} -> {self.game.pretty_game_name} ({self.id})'


class Game():
    """ Represents a table (or game). Example of json:
    {
     'table_id': '197451485', 'game_name': 'dicehospital', 'game_id': '1321', 
     'start': '1630119894', 'end': '1630123920', 'concede': '0', 'unranked': '0', 
     'normalend': '1', 'players': '85808177,90120944,89818831,86798513', 
     'player_names': 'araujoarthur0,barbara1508,dleite,tkcandrade', 'scores': '51,41,38,32', 
     'ranks': '1,2,3,4', 'elo_win': '0', 'elo_penalty': '', 'elo_after': '1363', 
     'arena_win': None, 'arena_after': '1.1500'
    }
    """
    def __init__(self, table_id, game_name, game_id, start, end, players, player_names, scores, ranks) -> None:
        self.table_id = table_id
        self.game_name = game_name
        self.pretty_game_name = get_pretty_name(self.game_name)
        self.game_id = game_id
        self.start = datetime.datetime.fromtimestamp(int(start))
        self.end = datetime.datetime.fromtimestamp(int(end))
        self.duration = self.end - self.start
        self.players = players
        self.player_names = player_names
        self.scores = scores
        self.ranks = ranks
    
    def __str__(self):
        return f'{self.game_name} ({self.game_id} - {self.duration})'