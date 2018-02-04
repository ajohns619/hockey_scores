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
    for i,result in enumerate(results):
        print(result[0] + ' ' + str(result[1]))
        if i%2 != 0:
            print("=============") 

def scrape_results(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    soup = BeautifulSoup(page.content, 'html.parser')



    scores = soup.find_all('td', class_='team-score')
    scores = [s.get_text() for s in scores]

    teams = soup.find_all('td', class_='team-name')
    teams = [t.get_text() for t in teams if valid_team(t.get_text())]

    results = zip(teams, scores)
    return results

def get_results():
    hockey_url = 'http://www.espn.com/nhl/scoreboard'
    hockey = scrape_results(hockey_url)
    
    pretty_print(hockey)


get_results()
