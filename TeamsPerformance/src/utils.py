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

DEBUG_MODE = True

URL = "http://google.com/"
MAX_WAIT_TIME = 30
HOME_IDX =  0
AWAY_IDX = CLK_IDX = 1

def debug_info(name,value):
    if DEBUG_MODE:
        print(colored(f"{name}:: {value}","yellow"))

league_date = datetime(2023, 8, 11)
def get_date(web_elm):
    info = web_elm.find_elements(By.CLASS_NAME, "imspo_mt__cmd")
    debug_info("info",info)
    if len(info) == 1:#for passed games
        date = info[0].find_element(By.XPATH, ".//span").text
        if "yesterday" in date.lower():
            date = (datetime.now() - timedelta(days=1)).strftime('%d %b %y')

    else:#for today or future games ()
        date = web_elm.find_element(By.CLASS_NAME, "imspo_mt__date").text
        if "today" in date.lower():
            date = datetime.now().strftime('%d %b %y')

    date = date.split(", ")[-1]
    if len(date.split(" ")) == 2:#if the format is d/m (without year) then we need to add the current year
        date += f" {datetime.now().year%1000}"
    #google issue§
    date = date.replace("Sept","Sep")
    time_info = web_elm.find_elements(By.CLASS_NAME, "imspo_mt__pm-infc")
    if len(time_info) and "TBD" not in time_info[CLK_IDX].text:
        return datetime.strptime(date + f" {time_info[CLK_IDX].text}", "%d %b %y %H:%M")
    debug_info("data_str",date)
    return datetime.strptime(date, "%d %b %y")

def web_elm_parser(web_elm):
    print(type(web_elm))
    match_dict = {}
    teams = web_elm.find_elements(By.CLASS_NAME, "liveresults-sports-immersive__hide-element")
    if not teams or '' == teams[0].text :
        return None
    #teams
    match_dict["home"] = teams[HOME_IDX].text
    match_dict["away"] = teams[AWAY_IDX].text
    #result
    results = web_elm.find_elements(By.CLASS_NAME, "imspo_mt__t-sc")
    if results:
        match_dict["result"] = ((results[HOME_IDX].text),(results[AWAY_IDX].text))
    else:
        match_dict["result"] = None

    #date
    date_object = get_date(web_elm)
    match_dict["date"] = date_object

    #league
    league = web_elm.find_elements(By.CLASS_NAME, "imspo_mt__lg-st-co")
    match_dict["league"] = "Local"
    if len(league):
        league = league[0].find_elements(By.XPATH, ".//span")[0].text
        match_dict["league"] = league
    #print("karam", match_dict["league"])

    return match_dict



def load_and_wait_wrapper(driver, by_elm, elm,multiple = False):
    if multiple:
        return WebDriverWait(driver, MAX_WAIT_TIME).until(
        EC.presence_of_all_elements_located((by_elm, elm)))
    else:
        return WebDriverWait(driver, MAX_WAIT_TIME).until(
        EC.presence_of_element_located((by_elm, elm)))


def start_session(driver, league, team):
    driver.get(URL)
    driver.maximize_window()
    search_box = driver.find_element(By.NAME, "q")
    search_query = f"{team} matches in {league}"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)


    #login()
