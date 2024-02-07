from TeamsPerformance.src.utils import *


def api_main(league, team):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en_UK'})
    driver = webdriver.Chrome(options=options)
    start_session(driver, league=league, team=team)
    #see_more = driver.find_element(By.XPATH, "//li[@data-tab_type='TEAM_MATCHES']")
    #print(see_more)
    if team == " ":
        see_more = load_and_wait_wrapper(driver, By.XPATH, "//li[@data-tab_type='LEAGUE_MATCHES']")
    else:
        see_more = load_and_wait_wrapper(driver, By.XPATH, "//li[@data-tab_type='TEAM_MATCHES']")
    see_more.send_keys(Keys.ENTER)
    sleep(5)
    print("scroll")
    loops = 10
    while True:
        for i in range(loops):
            driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)
        sleep(0.5)
        match = web_elm_parser(driver.switch_to.active_element)
        if match and match["date"] <= league_date:
            print(match["result"])
            break
    print("scroll2")
    # exit(0)
    elms = load_and_wait_wrapper(driver, By.CLASS_NAME, "liveresults-sports-immersive__match-tile",multiple=True)
    # elms = driver.find_elements(By.CLASS_NAME, "liveresults-sports-immersive__match-tile")

    # print(elms[0])
    # print(dir(elms[0]))
    sleep(5)
    matches = []
    for el in elms:
        sex = web_elm_parser(el)
        if sex is not None:
            matches.append(Match(sex))
    # matches = [Match(web_elm_parser(el)) for el in elms]
    for el in matches:
        print(el)