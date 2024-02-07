from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import timedelta
from TeamsPerformance.src.match import Match
from time import sleep
from termcolor import colored
import json
from TeamsPerformance.src.consts import *
from TeamsPerformance.src.league import League
import pdb
DEBUG_MODE = True

URL = "http://google.com/"
MAX_WAIT_TIME = 30
HOME_IDX =  0
AWAY_IDX = CLK_IDX = 1

def debug_info(name,value):
    if DEBUG_MODE:
        print(colored(f"{name}:: {value}","yellow"))

def is_local_league(web_elm,home: str , away: str) -> bool:
    #this class exists only for  champions league and local cup.
    competition = web_elm.find_elements(By.CLASS_NAME, COMPETITION_CLASS_NAME)
    if len(competition):
        return False
    # friendly matches are never between teams in the same league (when the class doesn't exist the  match is league or friendly)
    return (home in league_info.teams) and (away in league_info.teams)

def get_match_dict(web_elm):
    debug_info("get_match", "called")
    #check if this is an empty widget or the widget is a video
    if len(web_elm.find_elements(By.CLASS_NAME, WIDGET_CLASS_NAME)) == 0:
        debug_info("dict is None", "")
        return None

    #returns home : str , away : str or none if no teams in this web elem\
    def get_teams() -> (str,str):
        teams = web_elm.find_elements(By.CLASS_NAME, TEAMS_INFO_CLASS_NAME)
        debug_info("TEAMS",(teams[HOME_IDX].text, teams[AWAY_IDX].text))
        # teams
        return teams[HOME_IDX].text, teams[AWAY_IDX].text

    def get_result():
        results = web_elm.find_elements(By.CLASS_NAME, RESULTS_INFO_CLASS_NAME)
        if results:
            debug_info("RESULT", (results[HOME_IDX].text, results[AWAY_IDX].text))
            return results[HOME_IDX].text, results[AWAY_IDX].text
        return None

    def get_date()->str:
        info = web_elm.find_elements(By.CLASS_NAME, PASSED_DATE_INFO_CLASS_NAME)
        debug_info("info", info)
        if len(info) == 1:  # for passed games
            date = info[0].find_element(By.XPATH, SPAN_NAME).text
            if YESTERDAY_STR in date.lower():
                date = (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT_STR)

        else:  # for today or future games ()
            date_elms = web_elm.find_elements(By.CLASS_NAME, FUTURE_INFO_CLASS_NAME)
            if len(date_elms):
                date = date_elms[0].text
                if TODAY_STR in date.lower():
                    date = datetime.now().strftime(DATE_FORMAT_STR)
            else:#game is ongoing.
                date = datetime.now().strftime(DATE_FORMAT_STR)
        date = date.split(", ")[-1] # some date have day also (e.g. wed, <date>)
        date = date.replace("Sept","Sep")
        debug_info("date",date)
        return date

    match_dict = {}

    #teams
    match_dict["home"], match_dict["away"] = get_teams()

    #result
    match_dict["result"] = get_result()

    #date
    match_dict["date"] = get_date()

    return match_dict

def load_and_wait_wrapper(driver, by_elm, elm,multiple = False):
    if multiple:
        return WebDriverWait(driver, MAX_WAIT_TIME).until(
        EC.presence_of_all_elements_located((by_elm, elm)))
    else:
        return WebDriverWait(driver, MAX_WAIT_TIME).until(
        EC.presence_of_element_located((by_elm, elm)))


def start_session(driver, league, team):
    global league_info
    with open(LEAGUE_DATA_JSON_PATH, 'r') as f:
        json_leagues_info = json.load(f)
        league_info = League(teams=json_leagues_info[league]["teams"],
                             start_date=json_leagues_info[league]["start_date"],
                             end_date=json_leagues_info[league]["end_date"],
                             name=league)

    driver.get(URL)
    driver.maximize_window()
    search_box = driver.find_element(By.NAME, "q")
    search_query = f"{team} football matches in {league}"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)


    #login()

def get_matches(league, team):
    def get_local_matches():
        counter = (len(league_info.teams) -1) * 2
        sleep(5)
        while counter:
            driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)
            web_elem =  driver.switch_to.active_element
            match_dict = get_match_dict(web_elem)
            if match_dict and is_local_league(web_elem,match_dict["home"],match_dict["away"]):
                debug_info("counter",counter)
                counter -= 1
                yield match_dict
            # sleep(0.1)#FIXME :: add load

    def get_champions_matches():
        start_date = datetime.strptime(league_info.start_date,DATE_FORMAT_STR)
        sleep(5)
        while True:
            driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)
            web_elem = driver.switch_to.active_element
            match_dict = get_match_dict(web_elem)
            if match_dict is None:
                continue
            date_str = match_dict["date"]
            if len(date_str.split()) < 3:
                date_str = f'{date_str} {datetime.now().year % 1000}'
            debug_info("date", date_str)
            date = datetime.strptime(date_str,DATE_FORMAT_STR)
            if date < start_date:
                break
            if match_dict:
                if match_dict["home"] not in league_info.teams:
                    league_info.teams.append(match_dict["home"])
                yield match_dict

    def dates_fixer(matches : list) -> list:
        #convert date for str to datetime obj
        #matches are passed in descending order
        matches = reversed(matches)
        year = int(league_info.start_date.split()[2])
        flag = True
        for match in matches:
            if "Jan" in match.date and flag:
                year += 1
                flag = False
            day,month = match.date.split(" ")[0], match.date.split(" ")[1]
            month = "Sep" if month == "Sept" else month
            match.date = datetime.strptime(f"{day} {month} {year}",DATE_FORMAT_STR)
            yield match


    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en_UK'})
    driver = webdriver.Chrome(options=options)
    start_session(driver, league=league, team=team)

    if team == " ":
        see_more = load_and_wait_wrapper(driver, By.XPATH, SEE_MORE_NOT_LOCAL_LEAGUES_XPATH)
    else:
        see_more = load_and_wait_wrapper(driver, By.XPATH, SEE_MORE_LOCAL_LEAGUES_XPATH)
    see_more.send_keys(Keys.ENTER)

    if team != " ":#local
        to_ret = dates_fixer([Match(match_dict) for match_dict in get_local_matches()])
    else:#champions
        to_ret =  dates_fixer([Match(match_dict) for match_dict in get_champions_matches()])
    if DEBUG_MODE:
        print(colored("\n\n\n\nMATCHES:","yellow"))
        for match in to_ret:
            print(colored(match,"yellow"))
    return to_ret
    #FIXME :: add support for  champions , copa ......