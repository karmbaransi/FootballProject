from django.shortcuts import render, redirect
from TeamsPerformance.src.api import *
import json

# Create your views here.
def home(request):
    with open("TeamsPerformance/static/league_data.json", 'r') as f:
        leagues_info = json.load(f)
    if request.method == 'GET':
        return render(request, 'home.html', {'leagues_info':leagues_info})
    else:#calculate
        selected_team = request.POST["team_name"]
        selected_league = request.POST["leagues"]
        return redirect('performance', selected_league, selected_team)


def performance(request, selected_league, selected_team):
    if request.method == "GET":
        api_get_stats(league=selected_league, team=selected_team)
        return render(request, 'performance.html', {'team': selected_team, 'league': selected_league})

