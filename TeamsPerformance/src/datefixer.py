from datetime import datetime
from TeamsPerformance.src.consts import *

#when iterating the wedgites we pass each widget date to the date fixer and it returns datime obj for the date
#this class solves year issue
class DateFixer:
    def __init__(self, league):
        self.year = LAST_WIDGET_YEAR_DICT[league]
        self.jan_pass_flag = False
    def fix_Date(self,date : str):
        if "jan" in date.lower():
            self.jan_pass_flag = True
        if "jan" not in date.lower() and self.jan_pass_flag:
            self.jan_pass_flag = False
            self.year -= 1
        if len(date.split()) != 3:
            date += f" {self.year}"
        return datetime.strptime(date, DATE_FORMAT_STR)
