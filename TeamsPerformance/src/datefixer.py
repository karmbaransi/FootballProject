from datetime import datetime
from TeamsPerformance.src.consts import *

#when iterating the wedgites we pass each widget date to the date fixer and it returns datime obj for the date
#this class solves year issue
class DateFixer:
    def __init__(self):
        self.year = datetime.now().year % 1000
        self.jan_pass_flag = False
    def fix_Date(self,date : str):
            self.jan_pass_flag =  ("jan" in date.lower())
            if "jan" not in date.lower():
                self.jan_pass_flag = False
                self.year -= 1
            if len(date.split()) != 3:
                date += f" {self.year}"
            return datetime.strptime(date, DATE_FORMAT_STR)
