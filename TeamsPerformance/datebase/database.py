from  TeamsPerformance.models import Match as MatchDB,Team as TeamDB
from django.db.models import Q
from TeamsPerformance.src.match import Match as MatchInfo
import re

def db_get_team_info(sport,season,team):
    team_info = TeamDB.objects.filter(name=team,season=season,sport=sport)
    if len(team_info) == 0:#this is first time we call this team
        return None
    return team_info[0]

def db_update_team_info(sport,season,team,upcoming_match):
    team_info = TeamDB.objects.filter(name=team,season=season,sport=sport)
    if team_info.exists():
        if team_info[0].upcoming_match != upcoming_match:
            team_info[0].delete()
        else:
            return
    TeamDB.objects.create(
        name=team,
        upcoming_match=upcoming_match,
        season=season,
        sport=sport
    )

def db_add_matches(sport, season, league,matches):
    for match in matches:
        print(f"adding match: {match} to DB, res {match.result}")
        result = "None" if  match.result is None else match.result
        exists = MatchDB.objects.filter(
            home=match.home,
            away=match.away,
            date=match.date,
            league_name=league,
            season=season,
            sport=sport
        ).update(result=result)
        print(f"new change {exists}")
        if exists == 0: #match does not exist in the database
            new_match = MatchDB(
                                home=match.home,
                                away=match.away,
                                date=match.date,
                                result=result,
                                league_name=league,
                                season=season,
                                sport=sport)
            new_match.save()

def db_get_matches(sport, season, league,team):
    matches = MatchDB.objects.filter((Q(home=team) | Q(away=team)) & Q(season=season)
                                  & Q(league_name=league) & Q(sport=sport)).order_by("date")
    to_ret = []
    for match in matches:
        result = None
        if match.result != "None" :
            helper = re.findall(r"'(\d+)'",match.result)
            result = (helper[0],helper[1])
        to_ret.append(MatchInfo({'home':match.home,'away':match.away,'result':result,'date':match.date}))
    return to_ret