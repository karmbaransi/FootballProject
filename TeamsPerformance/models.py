from django.db import models

# Create your models here.
class Match(models.Model):
    home = models.CharField(max_length=20)
    away = models.CharField(max_length=20)
    date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=20)
    league_name = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    sport = models.CharField(max_length=20)

class Team(models.Model):
    name = models.CharField(max_length=20)
    upcoming_match = models.DateTimeField(null=True, blank=True)
    season = models.CharField(max_length=20)
    sport = models.CharField(max_length=20)