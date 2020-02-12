from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
from datetime import date
import time
from enum import Enum, auto
from models.betql_model import BetQLSpreadNCAAB
from models.betql_model import BetQLMoneylineNCAAB
from models.betql_model import BetQLTotalNCAAB
from models.betql_model import BetQL1stHalfSpreadNCAAB
from models.betql_model import BetQL1stHalfMoneylineNCAAB
from models.betql_model import BetQL1stHalfTotalNCAAB
from models.betql_model import BetQL2ndHalfSpreadNCAAB
from models.betql_model import BetQL2ndHalfMoneylineNCAAB
from models.betql_model import BetQLSpreadNBA
from models.betql_model import BetQLMoneylineNBA
from models.betql_model import BetQLTotalNBA
from models.betql_model import BetQL1stHalfSpreadNBA
from models.betql_model import BetQL1stHalfMoneylineNBA
from models.betql_model import BetQL1stHalfTotalNBA
from models.betql_model import BetQL2ndHalfSpreadNBA
from models.betql_model import BetQL2ndHalfMoneylineNBA
from database import session
from database import recreate_betql_table
from database import close_connection

browser = webdriver.Chrome('chromedriver.exe')
email = 'bonagamble@gmail.com'
password = 'Br@df0rd$$'


# login_res = requests.post('https://api.betql.co/graphql', json={"operationName": "login", "variables": {
# "email": email, "password": password}, "query": "mutation login($email: String!, $password: String!,
# $longitude: Float, " "$latitude: Float) {\n  login(username: $email, password: $password, " "longitude:
# $longitude, latitude: $latitude, product: \"bet\") {\n    token\n  " "  userId\n    sports {\n
# updatedTime\n      sport\n      __typename\n    " "}\n    __typename\n  }\n}\n"}, headers={'Content-Type':
# 'application/json'})
#
# token = login_res.json()['data']['login']['token']
# user_id = login_res.json()['data']['login']['userId']
class TabType(Enum):
    NCAAB_Spread = auto()
    NCAAB_Moneyline = auto()
    NCAAB_Total = auto()
    NCAAB_FirstHalfSpread = auto()
    NCAAB_FirstHalfMoneyline = auto()
    NCAAB_FirstHalfTotal = auto()
    NCAAB_SecondHalfSpread = auto()
    NCAAB_SecondHalfMoneyline = auto()
    NBA_Spread = auto()
    NBA_Moneyline = auto()
    NBA_Total = auto()
    NBA_FirstHalfSpread = auto()
    NBA_FirstHalfMoneyline = auto()
    NBA_FirstHalfTotal = auto()
    NBA_SecondHalfSpread = auto()
    NBA_SecondHalfMoneyline = auto()


def add_betql_spread_ncaab():
    browser.get('https://betql.co/ncaab/odds/spread')
    login_button = browser.find_element_by_xpath('//button[@class="rotoql-navbar__login-link"]')
    browser.execute_script('arguments[0].click()', login_button)
    login_tab = browser.find_element_by_class_name(
        'rotoql-login-modal__form-container').find_elements_by_tag_name('button')[0]
    browser.execute_script('arguments[0].click()', login_tab)
    browser.find_element_by_class_name('rotoql-login__form').find_element_by_name('email').send_keys(email)
    browser.find_element_by_class_name('rotoql-login__form').find_element_by_name('password').send_keys(password)
    browser.find_element_by_class_name('rotoql-login__form').submit()

    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB Spread Page is ready!")
    except TimeoutException:
        print("NCAAB Spread Loading took too much time!")
    time.sleep(15)
    print("NCAAB Spread Page is now live!")
    add_betql_data(TabType.NCAAB_Spread, 1)


def add_betql_moneyline_ncaab():
    browser.get('https://betql.co/ncaab/odds/moneyline')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB Moneyline Page is ready!")
    except TimeoutException:
        print("NCAAB Moneyline Loading took too much time!")
    time.sleep(8)
    print("NCAAB Moneyline Page is now live!")
    add_betql_data(TabType.NCAAB_Moneyline, 1)


def add_betql_total_ncaab():
    browser.get('https://betql.co/ncaab/odds/totals-spread')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB Total Page is ready!")
    except TimeoutException:
        print("NCAAB Total Loading took too much time!")
    time.sleep(8)
    print("NCAAB Total page is now live")
    add_betql_data(TabType.NCAAB_Total, 1)


def add_betql_first_half_spread_ncaab():
    browser.get('https://betql.co/ncaab/odds/first-half-lines')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB First Half Spread Page is ready!")
    except TimeoutException:
        print("NCAAB First Half Spread Loading took too much time!")
    time.sleep(8)
    print("NCAAB First Half Spread page is now live")
    add_betql_data(TabType.NCAAB_FirstHalfSpread, 1)


def add_betql_first_half_moneyline_ncaab():
    browser.get('https://betql.co/ncaab/odds/first-half-moneyline')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB First Half Moneyline Page is ready!")
    except TimeoutException:
        print("NCAAB First Half Moneyline Loading took too much time!")
    time.sleep(8)
    print("NCAAB First Half Moneyline Total page is now live")
    add_betql_data(TabType.NCAAB_FirstHalfMoneyline, 1)


def add_betql_first_half_total_ncaab():
    browser.get('https://betql.co/ncaab/odds/first-half-totals-spread')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB First Half Total Page is ready!")
    except TimeoutException:
        print("NCAAB First Half Total Loading took too much time!")
    time.sleep(8)
    print("NCAAB First Half Total Total page is now live")
    add_betql_data(TabType.NCAAB_FirstHalfTotal, 1)


def add_betql_second_half_spread_ncaab():
    browser.get('https://betql.co/ncaab/odds/second-half-lines')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB Second Half Spread Page is ready!")
    except TimeoutException:
        print("NCAAB Second Half Spread Loading took too much time!")
    time.sleep(8)
    print("NCAAB Second Half Spread Total page is now live")
    add_betql_data(TabType.NCAAB_SecondHalfSpread, 1)


def add_betql_second_half_moneyline_ncaab():
    browser.get('https://betql.co/ncaab/odds/second-half-moneylines')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NCAAB Second Half Moneyline Page is ready!")
    except TimeoutException:
        print("NCAAB Second Half Moneyline Loading took too much time!")
    time.sleep(8)
    print("NCAAB Second Half Moneyline Total page is now live")
    add_betql_data(TabType.NCAAB_SecondHalfMoneyline, 1)


def add_betql_spread_nba():
    browser.get('https://betql.co/nba/odds')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA Spread Page is ready!")
    except TimeoutException:
        print("NBA Spread Loading took too much time!")
    time.sleep(8)
    print("NBA Spread Page is now live!")
    add_betql_data(TabType.NBA_Spread, 0)


def add_betql_moneyline_nba():
    browser.get('https://betql.co/nba/odds/moneyline')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA Moneyline Page is ready!")
    except TimeoutException:
        print("NBA Moneyline Loading took too much time!")
    time.sleep(8)
    print("NBA Moneyline Page is now live!")
    add_betql_data(TabType.NBA_Moneyline, 0)


def add_betql_total_nba():
    browser.get('https://betql.co/nba/odds/totals-spread')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA Total Page is ready!")
    except TimeoutException:
        print("NBA Total Loading took too much time!")
    time.sleep(8)
    print("NBA Total Page is now live!")
    add_betql_data(TabType.NBA_Total, 0)


def add_betql_first_half_spread_nba():
    browser.get('https://betql.co/nba/odds/first-half-lines')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA First_Half_Spread Page is ready!")
    except TimeoutException:
        print("NBA First_Half_Spread Loading took too much time!")
    time.sleep(8)
    print("NBA First_Half_Spread Page is now live!")
    add_betql_data(TabType.NBA_FirstHalfSpread, 0)


def add_betql_first_half_moneyline_nba():
    browser.get('https://betql.co/nba/odds/first-half-moneyline')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA First_Half_Moneyline Page is ready!")
    except TimeoutException:
        print("NBA First_Half_Moneyline Loading took too much time!")
    time.sleep(8)
    print("NBA First_Half_Moneyline Page is now live!")
    add_betql_data(TabType.NBA_FirstHalfMoneyline, 0)


def add_betql_first_half_total_nba():
    browser.get('https://betql.co/nba/odds/first-half-totals-spread')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA First_Half_Total Page is ready!")
    except TimeoutException:
        print("NBA First_Half_Total Loading took too much time!")
    time.sleep(8)
    print("NBA First_Half_Total Page is now live!")
    add_betql_data(TabType.NBA_FirstHalfTotal, 0)


def add_betql_second_half_spread_nba():
    browser.get('https://betql.co/nba/odds/second-half-lines')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA Second_Half_Spread Page is ready!")
    except TimeoutException:
        print("NBA Second_Half_Spread Loading took too much time!")
    time.sleep(8)
    print("NBA Second_Half_Spread Page is now live!")
    add_betql_data(TabType.NBA_SecondHalfSpread, 0)


def add_betql_second_half_moneyline_nba():
    browser.get('https://betql.co/nba/odds/second-half-moneylines')
    try:
        myElem = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='games-table-column__team-link']")))
        print("NBA Second_Half_Moneyline Page is ready!")
    except TimeoutException:
        print("NBA Second_Half_Moneyline Loading took too much time!")
    time.sleep(8)
    print("NBA Second_Half_Moneyline Page is now live!")
    add_betql_data(TabType.NBA_SecondHalfMoneyline, 0)


def add_betql_data(tab_type, is_ncaab):
    data_list = []
    game_table_column = browser.find_element_by_class_name('games-container').find_elements_by_class_name(
        'games-table-column')[0]
    a_list = game_table_column.find_elements_by_xpath("//a[@class='games-table-column__team-link']")
    for col_a in a_list:
        if tab_type == TabType.NCAAB_Spread:
            new_betql = BetQLSpreadNCAAB()
        elif tab_type == TabType.NCAAB_Moneyline:
            new_betql = BetQLMoneylineNCAAB()
        elif tab_type == TabType.NCAAB_Total:
            new_betql = BetQLTotalNCAAB()
        elif tab_type == TabType.NCAAB_FirstHalfSpread:
            new_betql = BetQL1stHalfSpreadNCAAB()
        elif tab_type == TabType.NCAAB_FirstHalfMoneyline:
            new_betql = BetQL1stHalfMoneylineNCAAB()
        elif tab_type == TabType.NCAAB_FirstHalfTotal:
            new_betql = BetQL1stHalfTotalNCAAB()
        elif tab_type == TabType.NCAAB_SecondHalfSpread:
            new_betql = BetQL2ndHalfSpreadNCAAB()
        elif tab_type == TabType.NCAAB_SecondHalfMoneyline:
            new_betql = BetQL2ndHalfMoneylineNCAAB()
        elif tab_type == TabType.NBA_Spread:
            new_betql = BetQLSpreadNBA()
        elif tab_type == TabType.NBA_Moneyline:
            new_betql = BetQLMoneylineNBA()
        elif tab_type == TabType.NBA_Total:
            new_betql = BetQLTotalNBA()
        elif tab_type == TabType.NBA_FirstHalfSpread:
            new_betql = BetQL1stHalfSpreadNBA()
        elif tab_type == TabType.NBA_FirstHalfMoneyline:
            new_betql = BetQL1stHalfMoneylineNBA()
        elif tab_type == TabType.NBA_FirstHalfTotal:
            new_betql = BetQL1stHalfTotalNBA()
        elif tab_type == TabType.NBA_SecondHalfSpread:
            new_betql = BetQL2ndHalfSpreadNBA()
        elif tab_type == TabType.NBA_SecondHalfMoneyline:
            new_betql = BetQL2ndHalfMoneylineNBA()
        new_betql.Date = date.today()
        date_time = col_a.find_element_by_class_name('games-table-column__team-date-cell').get_attribute('innerHTML')
        date_time = date_time.split("<span")[0]
        print(date_time.split(', '))
        new_betql.Time = '' if len(date_time.split(', ')) <= 1 else date_time.split(', ')[1]
        team_list = col_a.find_elements_by_class_name('games-table-column__team-container')
        try:
            svg = team_list[0].find_element_by_tag_name('svg')
            new_betql.HomeFirst = 1
            new_betql.HomeTeam = team_list[0].find_element_by_class_name(
                'games-table-column__team-info-container').find_element_by_tag_name('p').get_attribute(
                'innerHTML').split("<span")[0]
            new_betql.AwayTeam = team_list[1].find_element_by_class_name(
                'games-table-column__team-info-container').find_element_by_tag_name('p').get_attribute(
                'innerHTML').split("<span")[0]
        except NoSuchElementException:
            new_betql.HomeFirst = 0
            new_betql.HomeTeam = team_list[1].find_element_by_class_name(
                'games-table-column__team-info-container').find_element_by_tag_name('p').get_attribute(
                'innerHTML').split("<span")[0]
            new_betql.AwayTeam = team_list[0].find_element_by_class_name(
                'games-table-column__team-info-container').find_element_by_tag_name('p').get_attribute(
                'innerHTML').split("<span")[0]
        data_list.append(new_betql)
    info_list = browser.find_element_by_class_name('sticky-container').find_elements_by_class_name('games-table-column')
    for info_index, info in enumerate(info_list):
        if is_ncaab:
            if info_index == 0:  # current-sp
                cell_list = info.find_elements_by_class_name('games-table-column__current-line-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_CurrentSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_CurrentSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 1:  # best bet rating
                cell_list = info.find_elements_by_class_name('games-table-column__value-rating-cell')
                for cell_index, cell in enumerate(cell_list):
                    rating_container = cell.find_elements_by_class_name('games-table-column__rating-container')[0] \
                        if data_list[cell_index].HomeFirst == 1 else \
                        cell.find_elements_by_class_name('games-table-column__rating-container')[1]
                    stars = rating_container.find_elements_by_tag_name('path')
                    rating = 0
                    for star in stars:
                        if star.value_of_css_property('fill') == 'rgb(255, 204, 1)':
                            rating += 1
                    data_list[cell_index].H_BetRating = str(rating)
                    data_list[cell_index].A_BetRating = '0'
            elif info_index == 2:  # Road O/U
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_RoadOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_RoadOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 3:  # Home O/U
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_HomeOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_HomeOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 4:  # Under %
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Under = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Under = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 5:  # Over %
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Over = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Over = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 6:  # Under Record
                cell_list = info.find_elements_by_class_name('games-table-column__under-record-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_UnderRecord = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_UnderRecord = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 7:  # Over Record
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OverRecord = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OverRecord = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 8:  # Net Units
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_NetUnits = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_NetUnits = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 9:  # Road
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Road = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Road = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 10:  # Home
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Home = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Home = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 11:  # Season Win %
                cell_list = info.find_elements_by_class_name('games-table-column__season-win-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_SeasonWin = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_SeasonWin = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 12:  # Games
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Games = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Games = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 13:  # ATS Units
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ATSUnits = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ATSUnits = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 14:  # Road ATS
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_RoadATS = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_RoadATS = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 15:  # Home ATS
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_HomeATS = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_HomeATS = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 16:  # ATS Win %
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ATSWin = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ATSWin = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 17:  # ATS Rec
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ATSRec = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ATSRec = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 18:  # Pro Edge-Sp
                cell_list = info.find_elements_by_class_name('games-table-column__pro-edge-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ProEdgeSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ProEdgeSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 19:  # U of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-under-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 20:  # O of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-over-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsO = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsO = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 21:  # ML of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-ml-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 22:  # SP of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-spread-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 23:  # Money % - SP
                cell_list = info.find_elements_by_class_name('games-table-column__money-percent-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_MoneySP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_MoneySP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 24:  # Ticket % - SP
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-percent-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 25:  # Line Move - O/U
                cell_list = info.find_elements_by_class_name('games-table-column__line-move-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_LineMoveOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_LineMoveOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 26:  # Line Move - ML
                cell_list = info.find_elements_by_class_name('games-table-column__line-move-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_LineMoveML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_LineMoveML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 27:  # Line Move - SP
                cell_list = info.find_elements_by_class_name('games-table-column__line-move-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_LineMoveSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_LineMoveSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 28:  # Open - O/U
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OpenOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OpenOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 29:  # Current - O/U
                cell_list = info.find_elements_by_class_name('games-table-column__current-ou-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_CurrentOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_CurrentOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 30:  # Open - ML
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OpenML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OpenML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 31:  # Current - ML
                cell_list = info.find_elements_by_class_name('games-table-column__current-ml-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_CurrentML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_CurrentML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 32:  # Open - SP
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OpenSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OpenSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
        else:
            if info_index == 0:  # current-sp
                cell_list = info.find_elements_by_class_name('games-table-column__current-line-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_CurrentSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_CurrentSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 1:  # best bet rating
                cell_list = info.find_elements_by_class_name('games-table-column__value-rating-cell')
                for cell_index, cell in enumerate(cell_list):
                    rating_container = cell.find_elements_by_class_name('games-table-column__rating-container')[0] \
                        if data_list[cell_index].HomeFirst == 1 else \
                        cell.find_elements_by_class_name('games-table-column__rating-container')[1]
                    stars = rating_container.find_elements_by_tag_name('path')
                    rating = 0
                    for star in stars:
                        if star.value_of_css_property('fill') == 'rgb(255, 204, 1)':
                            rating += 1
                    data_list[cell_index].H_BetRating = str(rating)
                    data_list[cell_index].A_BetRating = '0'
            elif info_index == 2:  # Points Against
                cell_list = info.find_elements_by_class_name('games-table-column__pts-against-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_PointsAgainst = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_PointsAgainst = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 3:  # Points For
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_PointsFor = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_PointsFor = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 4:  # Pro Edge-Sp
                cell_list = info.find_elements_by_class_name('games-table-column__pro-edge-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ProEdgeSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ProEdgeSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 5:  # U of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-under-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 6:  # O of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-over-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsO = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsO = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 7:  # ML of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-ml-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 8:  # Sp of Tickets
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-count-spread-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketsSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketsSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 9:  # Money % -Sp
                cell_list = info.find_elements_by_class_name('games-table-column__money-percent-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_MoneySP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_MoneySP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 10:  # Ticket % -Sp
                cell_list = info.find_elements_by_class_name('games-table-column__ticket-percent-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_TicketSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_TicketSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 11:  # Road O/U
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_RoadOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_RoadOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 12:  # Home O/U
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_HomeOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_HomeOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 13:  # Under %
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Under = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Under = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 14:  # Over %
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Over = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Over = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 15:  # Under Record
                cell_list = info.find_elements_by_class_name('games-table-column__under-record-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_UnderRecord = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_UnderRecord = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 16:  # Over Record
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OverRecord = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OverRecord = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 17:  # ATS Units
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ATSUnits = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ATSUnits = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 18:  # Road ATS
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_RoadATS = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_RoadATS = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 19:  # Home ATS
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_HomeATS = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_HomeATS = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 20:  # ATS Win %
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ATSWin = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ATSWin = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 21:  # ATS Rec
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_ATSRec = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_ATSRec = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 22:  # Net Units
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_NetUnits = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_NetUnits = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 23:  # Road
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Road = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Road = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 24:  # Home
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Home = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Home = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 25:  # Season Win %
                cell_list = info.find_elements_by_class_name('games-table-column__season-win-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_SeasonWin = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_SeasonWin = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 26:  # Games
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_Games = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_Games = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 27:  # Line Move - O/U
                cell_list = info.find_elements_by_class_name('games-table-column__line-move-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_LineMoveOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_LineMoveOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 28:  # Line Move - ML
                cell_list = info.find_elements_by_class_name('games-table-column__line-move-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_LineMoveML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_LineMoveML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 29:  # Line Move - Sp
                cell_list = info.find_elements_by_class_name('games-table-column__line-move-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_LineMoveSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_LineMoveSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 30:  # Open - O/U
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OpenOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OpenOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 31:  # Current - O/U
                cell_list = info.find_elements_by_class_name('games-table-column__current-ou-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_CurrentOU = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_CurrentOU = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 32:  # Open - ML
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OpenML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OpenML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 33:  # Current - ML
                cell_list = info.find_elements_by_class_name('games-table-column__current-ml-cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_CurrentML = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_CurrentML = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
            elif info_index == 33:  # Open - Sp
                cell_list = info.find_elements_by_class_name('games-table-column__cell')
                for cell_index, cell in enumerate(cell_list):
                    data_list[cell_index].H_OpenSP = cell.find_elements_by_tag_name('p')[0].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[1].get_attribute('innerHTML')
                    data_list[cell_index].A_OpenSP = cell.find_elements_by_tag_name('p')[1].get_attribute(
                        'innerHTML') if data_list[cell_index].HomeFirst == 1 else cell.find_elements_by_tag_name(
                        'p')[0].get_attribute('innerHTML')
        print(info_index+1)

    session.add_all(data_list)


recreate_betql_table()
add_betql_spread_ncaab()
add_betql_moneyline_ncaab()
add_betql_total_ncaab()
add_betql_first_half_spread_ncaab()
add_betql_first_half_moneyline_ncaab()
add_betql_first_half_total_ncaab()
add_betql_second_half_spread_ncaab()
add_betql_second_half_moneyline_ncaab()
add_betql_spread_nba()
add_betql_first_half_spread_nba()
add_betql_first_half_moneyline_nba()
add_betql_first_half_total_nba()
add_betql_second_half_spread_nba()
add_betql_second_half_moneyline_nba()

session.commit()
browser.close()
close_connection()
