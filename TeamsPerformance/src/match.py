from TeamsPerformance.src.consts import DATE_FORMAT_STR

class Match:
    def __init__(self, info):
        self.home = info["home"]
        self.away = info["away"]
        self.date = info["date"]
        self.result = info["result"]

    def __str__(self):
        result = ",TBD," if self.result is None else f"{self.result[0]},-,{self.result[1]}"
        return f"{self.home},{self.away},{result},{self.date.strftime(DATE_FORMAT_STR)}"
