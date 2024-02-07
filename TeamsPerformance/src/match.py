from TeamsPerformance.src.consts import DATE_FORMAT_STR

class Match:
    def __init__(self, info):
        self.home = info["home"]
        self.away = info["away"]
        self.date = info["date"]
        self.result = info["result"]

    def __str__(self):
        return f"{self.home} VS. {self.away} - {self.result} : {self.date.strftime(DATE_FORMAT_STR)}"
