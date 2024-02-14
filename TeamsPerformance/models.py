from django.db import models

# Create your models here.
class Match(models.Model):
    home = models.CharField(max_length=20)
    away = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    result = models.CharField(max_length=20)
    league_name = models.CharField(max_length=20)
    season = models.CharField(max_length=20)