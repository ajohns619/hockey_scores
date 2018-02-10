#! /usr/bin/env python3
import re
from lxml import html
import requests
from bs4 import BeautifulSoup
import argparse
import datetime



def valid_team(team_name):
    if re.match("^[A-Za-z ]*$", team_name):
        return True
    return False

def pretty_print(results):
    print("=============")

    for i,game in enumerate(results):
        print(game[2]) # Game State
        print(game[0][0] + ' ' + str(game[1][0])) # Away Team Name and Score
        print(game[0][1] + ' ' + str(game[1][1])) # Home Team Name and Score
        print("=============") 


""" Creates a list of zip objects with the following format:
    <(away_team, home_team), (away_score, home_score), game_state>
"""
def construct_results(teams, scores, games_info):
    return list(zip(teams, scores, games_info))

def scrape_results(url, scrape_func, *args, **kwargs):
    if (kwargs['tomorrow']):
        date = datetime.date.today() + datetime.timedelta(days=1)
        date = date.strftime("%Y%m%d")
    elif (kwargs['yesterday']):
        date = datetime.date.today() - datetime.timedelta(days=1)
        date = date.strftime("%Y%m%d")
    elif (kwargs['custom']):
        date = kwargs['custom']
    else:
        date = datetime.datetime.now().strftime("%Y%m%d")

    page = requests.get(url + '?date=' + date)
    tree = html.fromstring(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')

    return scrape_func(soup)


def nhl_scrape_results(soup):
    scores = soup.find_all('td', class_='team-score')
    scores = [s.getText() for s in scores]

    teams = soup.find_all('td', class_='team-name')
    teams = [t.getText() for t in teams if valid_team(t.getText())]

    games_info = soup.find_all('ul', class_='game-info')
    games_info = [g.getText(separator=u' ').replace('\xa0', '') for g in games_info]
    games_info = [g[1:] if g[0] == ' ' else g for g in games_info]

    teams = zip(teams[::2], teams[1::2])
    scores = zip(scores[::2], scores[1::2])
    
    return construct_results(teams, scores, games_info)



def get_results(*args, **kwargs):
    hockey_url = 'http://www.espn.com/nhl/scoreboard'
    nhl_results = scrape_results(hockey_url, nhl_scrape_results, **kwargs)
    pretty_print(nhl_results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tomorrow", help="use tomorrow's date", action="store_true")
    parser.add_argument("-y", "--yesterday", help="use yesterday's date", action="store_true")
    parser.add_argument("-c", "--custom", help="enter custom date, format: YYYYMMDD")
    
    args = parser.parse_args()

    get_results(tomorrow=args.tomorrow, yesterday=args.yesterday, custom=args.custom)




