import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import certifi
import pdb
from datetime import datetime
import re
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
import sqlalchemy
import mysql.connector



def writing(commentary_details):
	engine = create_engine("mysql://root:@127.0.0.1/Football",echo=False)
	commentary_details.to_sql(name='Live_commentary', con=engine, if_exists = 'append', index=False)

def word_cloud(commentary):
	wordcloud = WordCloud(font_path='/Library/Fonts/Verdana.ttf',
                      relative_scaling = 1.0,
                      stopwords = stopwords
                      ).generate(commentary)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

def aggregate_commentary(commentary,player_commentary_agg):
	player_commentary_agg = player_commentary_agg + commentary[0][1]
	return player_commentary_agg


def get_player_text(commentary):
	if player in commentary[1]:
		return True

def getText(node):
	return node.text.encode('utf-8').decode('ascii','ignore')

def cleanText(text):
	text = text.replace('\n','')
	commentary = int(text.find('mins:'))
	if commentary != -1:
		return (commentary,text[text.find('mins:')+5:])
	else:
		return (commentary,text)

def teams_involved(url):
	content = urllib2.urlopen(url,cafile=certifi.where()).read()
	soup = BeautifulSoup(content,"lxml")
	teams = soup.find_all(class_ = 'block-title')[0].text
	home_team = teams[13:].split("-")[0][:-2]
	away_team = teams[13:].split("-")[1][2:]
	return (teams[teams.find(":")+2:].split(' '),home_team,away_team)


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

def list_to_dataframe(player_details_list):
	player_details_df = pd.DataFrame(np.array(player_details_list).reshape(1,5),columns = ['player_commentary','player_name','home_team','away_team','was_home'])
	return player_details_df


unwanted_words = ['Reuters','Getty','Photograph']
url = 'https://www.theguardian.com/football/live/2018/may/10/west-ham-united-v-manchester-united-premier-league-live'


commentary = get_commentary(url)
players = get_player_names(commentary[-2][1])

#Last two values of tuples gives team news. Not necessary.
commentary = commentary[:-2]


mapping = map(mapping_commentary_to_players,commentary)

stopwords_teams = teams_involved(url)[0]
home_team = teams_involved(url)[1]
away_team = teams_involved(url)[2]

player = 'Arnautovic'
player_commentary = filter(get_player_text,mapping)

player_commentary_agg = ''
player_commentary_agg = map(lambda x:aggregate_commentary(x,player_commentary_agg),player_commentary)

player_commentary_agg = ('').join(player_commentary_agg)
player_details_list = [player_commentary_agg,player,home_team,away_team,1]

player_details_df = list_to_dataframe(player_details_list)
writing(player_details_df)


stopwords = set(STOPWORDS)
stopwords.add(player)
stopwords.add(player+'s')
stopwords.update(stopwords_teams)
stopwords.update(unwanted_words)

# word_cloud(player_commentary_agg)






