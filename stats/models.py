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
