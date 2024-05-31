from django.shortcuts import render, redirect
from TeamsPerformance.src.api import *
from TeamsPerformance.src.custom_exception import LoggableException
import json
from termcolor import colored
from TeamsPerformance.datebase.database import get_recently_called_matches

from .models import Match

# Create your views here.
G_is_dark = None
def home(request):

    recently_called = get_recently_called_matches()
    global G_is_dark
    if G_is_dark is None:
        G_is_dark = 1
    with open("TeamsPerformance/static/league_data.json", 'r') as f:
        leagues_info = json.load(f)
    if request.method == 'GET':
        return render(request, 'home.html', {'leagues_info':leagues_info, 'recently_called': recently_called,'is_dark': G_is_dark})
    else:#calculate
        selected_season = request.POST["season"]
        selected_sport = request.POST["sports"]
        selected_team = request.POST["team_name"]
        selected_league = request.POST["leagues"]
        G_is_dark = request.POST["is_dark"]
        return redirect('performance', selected_season, selected_sport, selected_league, selected_team,G_is_dark)



def performance(request, selected_season, selected_sport, selected_league, selected_team,is_dark):
    try:
        if request.method == "GET":
            stats = api_get_stats(season=selected_season, sport=selected_sport ,league=selected_league, team=selected_team)
            return render(request, 'local_league_performance.html', {'season': selected_season,'sport' : selected_sport,'team': selected_team, 'league': selected_league,'stats': stats,'is_dark': is_dark})


    except LoggableException as e:
        err_msg =  f"{e}."
        return render(request,'error_page.html', {'err_msg': err_msg})
    except Exception as e:
        print(colored(f"ERROR: {e}","red"))
        err_msg = ""
        return render(request, 'error_page.html', {'err_msg': err_msg, 'season': selected_season,'sport' : selected_sport,'team': selected_team, 'league': selected_league})

