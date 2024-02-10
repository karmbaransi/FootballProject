from TeamsPerformance.src.utils import get_matches
from TeamsPerformance.src.utils import debug_info
from TeamsPerformance.src.match import Match
from TeamsPerformance.src.consts import *

def api_get_matches_results(league,team):
    return get_matches(league, team)
def api_get_stats(league, team):
    def get_gained_points(match_info : Match):#FIXME:: penalties support + points to gain to the consts
        if int(match_info.result[0]) >  int(match_info.result[1]):
            return 3 if match_info.home == team else 0
        elif int(match_info.result[0]) <  int(match_info.result[1]):
            return 0 if match_info.home == team else 3
        else:#draw
            return 1
    def get_out_in_goals(match_info : Match):#FIXME:: penalties support
        if match_info.home == team:
            return int(match_info.result[0]),int(match_info.result[1])
        else:
            return int(match_info.result[1]),int(match_info.result[0])
    stats = {"points_graph": [],"in_goals" : [],"out_goals": [], "matches":[]}#FIXME:: (names + add to consts)
    matches =  api_get_matches_results(league,team)
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


