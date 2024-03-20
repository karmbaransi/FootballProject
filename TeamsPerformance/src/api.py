from TeamsPerformance.src.utils import get_matches, get_league_info
from TeamsPerformance.src.utils import debug_info
from TeamsPerformance.src.match import Match
from TeamsPerformance.src.consts import *
from datetime import datetime
from TeamsPerformance.datebase.database import *

def api_get_matches_results(season,sport,league,team):#FIXME add checkup in the DB
    team_info = db_get_team_info(sport=sport, season=season, team=team)
    if team_info is None:
        matches = get_matches(season, sport, league, team)
    else:
        matches = get_matches(season, sport, league, team,upcoming_date=team_info.upcoming_match)
    db_add_matches(sport=sport,season=season,league=league,matches=matches)
    matches = db_get_matches(sport=sport,season=season,league=league,team=team)
    up_coming = datetime.max
    for match in matches:
        if match.result is None:
            up_coming = match.date
            break

    db_update_team_info(sport=sport,season=season,team=team,upcoming_match=up_coming)
    return  matches
def api_get_local_league_stats(season,sport,league, team):
    def get_gained_points(match_info : Match):#FIXME:: penalties support + points to gain to the consts
        league_info = get_league_info()
        if match_info.result[0] is None:
            return 0
        if int(match_info.result[0]) >  int(match_info.result[1]):
            return league_info.point_rules["win"] if match_info.home == team else league_info.point_rules["lose"]
        elif int(match_info.result[0]) <  int(match_info.result[1]):
            return league_info.point_rules["lose"] if match_info.home == team else league_info.point_rules["win"]
        else:#draw
            return league_info.point_rules["draw"]
    def get_out_in_goals(match_info : Match):#FIXME:: penalties support
        if match_info.home == team:
            return int(match_info.result[0]),int(match_info.result[1])
        else:
            return int(match_info.result[1]),int(match_info.result[0])
    stats = {"points_graph": [],"in_goals" : [],"out_goals": [], "matches":[]}#FIXME:: (names + add to consts)
    matches =  api_get_matches_results(season,sport,league,team)
    curr_out_goals,curr_in_goals,curr_points = 0,0,0
    for match in matches:
        debug_info("match info",match)
        if match.result is not None:
            curr_points += get_gained_points(match)
            date = match.date.strftime(DATE_FORMAT_STR)
            out_goals,in_goals = get_out_in_goals(match)
            curr_in_goals += in_goals
            curr_out_goals += out_goals
            stats["points_graph"].append({"x": date, "y": curr_points})
            stats["in_goals"].append({"x": date, "y": curr_in_goals})
            stats["out_goals"].append({"x": date, "y": curr_out_goals})
        stats["matches"].append(f"{match}")
        debug_info("(p,o,i)",(curr_points,curr_out_goals,curr_in_goals))
    return stats

def api_get_stats(season,sport, league, team):
    return api_get_local_league_stats(season,sport, league, team)