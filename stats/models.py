from django.db import models
import datetime

from .prettifier import get_pretty_name

from django.db import models

class PlayerModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name} ({self.id})' 

class GameModel(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey('PlayerModel', on_delete=models.CASCADE, related_name='current_player', null=True, blank=True)
    table_id = models.IntegerField(default=0)
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

    def players_as_list(self):
        return self.players.split(',')

    def player_names_as_list(self):
        return self.player_names.split(',')

    def scores_as_list(self):
        return self.scores.split(',')

    def ranks_as_list(self):
        return self.ranks.split(',')
    
    def final_elo(self):
        # For some reason, BGA stored initial ELO (0) as 1300
        # So we need some math to get the final visible ELO
        return (self.elo_after - 1300)

    def __str__(self):
        return f'{self.player.name} -> {self.pretty_game_name} ({self.table_id})' 
