from django.shortcuts import render, redirect
from TeamsPerformance.src.api import *
import json
from .models import Match

# Create your views here.
def home(request):
    with open("TeamsPerformance/static/league_data.json", 'r') as f:
        leagues_info = json.load(f)
    if request.method == 'GET':
        return render(request, 'home.html', {'leagues_info':leagues_info})
    else:#calculate
        selected_season = request.POST["season"]
        selected_sport = request.POST["sports"]
        selected_team = request.POST["team_name"]
        selected_league = request.POST["leagues"]
        return redirect('performance', selected_season, selected_sport, selected_league, selected_team)


def performance(request, selected_season, selected_sport, selected_league, selected_team):
    if request.method == "GET":
        stats = api_get_stats(season=selected_season, sport=selected_sport ,league=selected_league, team=selected_team)
        return render(request, 'local_league_performance.html', {'sport' : selected_sport,'team': selected_team, 'league': selected_league,'stats': stats})

