import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import certifi
from datetime import datetime


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
	nav = soup.find_all("div",{"class":"liveblog-navigation__older"})[0].find_all("a")[0].get("href")
	commentary = map(cleanText, map(getText, soup.find_all("div", {"class": "block-elements"})))
	print commentary
	print 'NEXT'
	if nav:
		commentary.extend(get_commentary("https://www.theguardian.com/"+nav))
	
	return commentary

url = 'https://www.theguardian.com/football/live/2018/may/10/west-ham-united-v-manchester-united-premier-league-live'

commentary = get_commentary(url)

