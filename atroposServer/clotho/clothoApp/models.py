from django.db import models

class Telling(models.Model):
    player1NodeId = models.IntegerField(default=0)
    player2NodeId = models.IntegerField(default=0)
