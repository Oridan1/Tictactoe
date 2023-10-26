from django.db import models

class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    board = models.JSONField(default=[[None, None, None], [None, None, None], [None, None, None]])
    players = models.ManyToManyField('Player', related_name='games')
    winner = models.CharField(max_length=255, blank=True, null=True)
    movements_played = models.IntegerField(default=0)
    next_turn = models.CharField(max_length=255)

class Player(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=1)
    
    def __str__(self):
        return self.name
