import datetime


class Match:
    def __init__(self, info):
        self.home = info["home"]
        self.away = info["away"]
        self.date = info["date"]
        self.league = info["league"]
        self.result = info["result"]
