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
from TeamsPerformance.src.datefixer import DateFixer
from TeamsPerformance.src.custom_exception import LoggableException
from selenium.webdriver.chrome.service import Service
from copy import deepcopy

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
        print("helper", competition[0].text)
        if "NBA Cup" not in competition[0].text:
            return False
    # friendly matches are never between teams in the same league (when the class doesn't exist the  match is league or friendly)
    return (home in league_info.teams) and (away in league_info.teams)

def get_match_dict(web_elm):
    debug_info("get_match", "called")
    # check if this is an empty widget or the widget is a video
    if len(web_elm.find_elements(By.CLASS_NAME, EMPTY_TILE_CLASS_NAME)):
        print("caught an empty tile")
        return None

    #check if this is an empty widget or the widget is a video
    if len(web_elm.find_elements(By.CLASS_NAME, WIDGET_CLASS_NAME)) == 0:
        debug_info("dict is None", "")
        return None

    #returns home : str , away : str or none if no teams in this web elem\
    def get_teams() -> (str,str):
        teams = web_elm.find_elements(By.CLASS_NAME, TEAMS_INFO_CLASS_NAME)
        debug_info("TEAMS",(teams[HOME_IDX].text.split("\n")[0], teams[AWAY_IDX].text.split("\n")[0]))
        # teams
        return teams[HOME_IDX].text.split("\n")[0], teams[AWAY_IDX].text.split("\n")[0]

    def get_result():
        results = web_elm.find_elements(By.CLASS_NAME, RESULTS_INFO_CLASS_NAME)
        if results:
            debug_info("RESULT", (results[HOME_IDX].text, results[AWAY_IDX].text))
            return results[HOME_IDX].text, results[AWAY_IDX].text
        return None

    def get_date():
        info = web_elm.find_elements(By.CLASS_NAME, PASSED_DATE_INFO_CLASS_NAME)
        debug_info("info", info)
        if len(info) == 1:  # for passed games
            date = info[0].find_element(By.XPATH, SPAN_NAME).text.replace(",", "")
            print("new date str :: ",date)
            debug_info("get_date():date",date)
            if YESTERDAY_STR in date.lower():
                date = (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT_STR)
            if TODAY_STR in date.lower():
                date = datetime.now().strftime(DATE_FORMAT_STR)
        else:  # for today or future games ()
            date_elms = web_elm.find_elements(By.CLASS_NAME, FUTURE_INFO_CLASS_NAME)
            if len(date_elms):
                date = date_elms[0].text
                if TODAY_STR in date.lower():
                    date = datetime.now().strftime(DATE_FORMAT_STR)
                if TOMORROW_STR in date.lower():
                    date = (datetime.now() + timedelta(days=1)).strftime(DATE_FORMAT_STR)
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
    print("match_dict", match_dict)

    if '' in list(match_dict.values()):
        return None
    return match_dict

def load_and_wait_wrapper(driver, by_elm, elm,multiple = False):
    try:
        if multiple:
            return WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_all_elements_located((by_elm, elm)))
        else:
            return WebDriverWait(driver, MAX_WAIT_TIME).until(
            EC.presence_of_element_located((by_elm, elm)))
    except Exception as e:
        print("exception :::: ",e)
        raise LoggableException(f"Please check your internet connection and the json syntax")

def start_session(driver,season, sport, league, team):
    driver.get(URL)
    sleep(3)
    for i in range(20):
        driver.switch_to.active_element.send_keys(Keys.TAB)
        web_elem = driver.switch_to.active_element
        if web_elem.text in ["Accept all"]:
            web_elem.send_keys(Keys.ENTER)
            break
    sleep(3)
    # driver.maximize_window()
    search_box = driver.find_element(By.NAME, "q")
    search_query = f"{team} {sport} matches in {league}"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)


    #login() 

def get_matches(season, sport, league, team,upcoming_date=None):
    def get_local_matches():
        sleep(5)
        date_fixer = DateFixer(league)
        end_date = datetime.strptime(league_info.end_date,DATE_FORMAT_STR)
        stop_date = datetime.strptime(league_info.start_date,DATE_FORMAT_STR)
        if upcoming_date:
            stop_date = upcoming_date
        to_ret = []
        elems_dict = []
        while True:
            print("1")
            web_elem =  driver.switch_to.active_element
            print("2")
            print("web elem class::", web_elem.get_attribute('class'))
            if web_elem.get_attribute('class') != WIDGET_IDENTIFIER:
                elems_dict.append(web_elem)
            while web_elem in elems_dict:
                print("elm is in dict")
                driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)
                print("3")
                web_elem = driver.switch_to.active_element
                print("4")
                if web_elem == elems_dict[-1]:
                    print("sleeping ,match dict")# , get_match_dict(web_elem))
                    sleep(7)

            elems_dict.append(web_elem)
            print("5")
            match_dict = get_match_dict(web_elem)
            print("6")
            if match_dict is None:
                continue
            match_dict["date"] = deepcopy(date_fixer.fix_Date(match_dict["date"]))
            print("7")
            debug_info("get_local_matches , match",match_dict)
            if match_dict["date"] > end_date:
                continue
            if match_dict["date"].date() < stop_date.date():
                break
            if is_local_league(web_elem,match_dict["home"],match_dict["away"]):
                to_ret.append(match_dict)
            sleep(0.1)
            driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)
        return to_ret

    global league_info
    with open(LEAGUE_DATA_JSON_PATH, 'r') as f:
        json_sports_info = json.load(f)
        json_leagues_info = json_sports_info["sports"][sport][season]["leagues"]
        league_info = League(teams=json_leagues_info[league]["teams"],
                             start_date=json_leagues_info[league]["start_date"],
                             end_date=json_leagues_info[league]["end_date"],
                             name=league, point_rules=json_sports_info["points"][sport])

    if upcoming_date is not None:
        debug_info("upcoming_date.date(),datetime.now().date()",(upcoming_date.date(),datetime.now().date()))
        if upcoming_date.date() > datetime.now().date():
            return []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en_UK'})
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    # options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-running-insecure-content')
    # # options.add_argument("--disable-extensions")

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--accept-lang=en_UK")
    driver = webdriver.Chrome(options=options)
    # driver.minimize_window()
    start_session(driver,season=season, sport=sport, league=league, team=team)
    sleep(3)

    # see_more = load_and_wait_wrapper(driver, By.XPATH, SEE_MORE_LOCAL_LEAGUES_XPATH)
    while True:
        driver.switch_to.active_element.send_keys(Keys.TAB)
        web_elem = driver.switch_to.active_element
        if web_elem.text in ["More matches","See more"]:
            web_elem.send_keys(Keys.ENTER)
            break
    to_ret = reversed([Match(match_dict) for match_dict in get_local_matches()])
    return to_ret

def get_league_info():
    return league_info