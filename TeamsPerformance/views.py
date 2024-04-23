from django.shortcuts import render, redirect
from TeamsPerformance.src.api import *
from TeamsPerformance.src.custom_exception import LoggableException
import json
from termcolor import colored
from TeamsPerformance.datebase.database import get_recently_called_matches

from .models import Match

# Create your views here.
def home(request):

    recently_called = get_recently_called_matches()

    with open("TeamsPerformance/static/league_data.json", 'r') as f:
        leagues_info = json.load(f)
    if request.method == 'GET':
        return render(request, 'home.html', {'leagues_info':leagues_info, 'recently_called': recently_called})
    else:#calculate
        selected_season = request.POST["season"]
        selected_sport = request.POST["sports"]
        selected_team = request.POST["team_name"]
        selected_league = request.POST["leagues"]
        return redirect('performance', selected_season, selected_sport, selected_league, selected_team)



def performance(request, selected_season, selected_sport, selected_league, selected_team):
    try:
        if request.method == "GET":
            stats = api_get_stats(season=selected_season, sport=selected_sport ,league=selected_league, team=selected_team)
            return render(request, 'local_league_performance.html', {'season': selected_season,'sport' : selected_sport,'team': selected_team, 'league': selected_league,'stats': stats})
    except LoggableException as e:
        err_msg =  f"{e}"
        return render(request,'error_page.html', {'err_msg': err_msg})
    except Exception as e:
        print(colored(f"ERROR: {e}","red"))
        err_msg = ""
        return render(request, 'error_page.html', {'err_msg': err_msg})

