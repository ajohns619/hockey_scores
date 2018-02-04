#! /usr/bin/env python3
import re
from lxml import html
import requests
from bs4 import BeautifulSoup

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

def scrape_results(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    soup = BeautifulSoup(page.content, 'html.parser')



    scores = soup.find_all('td', class_='team-score')
    scores = [s.get_text() for s in scores]

    teams = soup.find_all('td', class_='team-name')
    teams = [t.get_text() for t in teams if valid_team(t.get_text())]

    games_info = soup.find_all('ul', class_='game-info')
    games_info = [g.get_text().replace('\xa0', '') for g in games_info]

    teams = zip(teams[::2], teams[1::2])
    scores = zip(scores[::2], scores[1::2])
   
    """Creates a list of zip objects with the following format:
       <(away_team, home_team), (away_score, home_score), game_state>
    """
    results = list(zip(teams, scores, games_info))
    
    return results

def get_results():
    hockey_url = 'http://www.espn.com/nhl/scoreboard'
    hockey = scrape_results(hockey_url)
    pretty_print(hockey)



get_results()
