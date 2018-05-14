import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import certifi
import pdb
from datetime import datetime
import re


# def get_team_names():

def getText(node):
	return node.text.encode('utf-8').decode('ascii','ignore')

def cleanText(text):
	text = text.replace('\n','')
	commentary = int(text.find('mins:'))
	if commentary != -1:
		return (commentary,text[text.find('mins:')+5:])
	else:
		return (commentary,text)


def get_commentary(url):
	content = urllib2.urlopen(url,cafile=certifi.where()).read()
	soup = BeautifulSoup(content,"lxml")
	nav = soup.find_all(class_ = "liveblog-navigation__older")[0].find_all("a")[0].get("href")
	commentary = map(cleanText, map(getText, soup.find_all(class_ = "block-elements")))
	if nav:
		commentary.extend(get_commentary("https://www.theguardian.com/"+nav))
	return commentary

def get_player_names(commentary):
	players_regex = re.findall('([a-zA-Z]+)(,|\.)', str(commentary[commentary.find(":"):commentary.find("Referee")]))
	players = [names[0] for names in players_regex]
	return players

def mapping_commentary_to_players(commentary):
	active_players = [player for player in players if player in commentary[1]]
	return (commentary,active_players)

url = 'https://www.theguardian.com/football/live/2018/may/10/west-ham-united-v-manchester-united-premier-league-live'
commentary = get_commentary(url)
players = get_player_names(commentary[-2][1])
mapping = map(mapping_commentary_to_players,commentary)




