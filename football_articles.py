import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import certifi
from datetime import datetime
import os


year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%b').lower()
day = datetime.now().strftime('%d')
time = ('/').join([year,month,day])
article = []

while True:
	for author in ['Jonathan Wilson','Sid Lowe','Daniel Taylor','Sachin Nakrani','Amy Lawrence','Barney Ronay']:
		url = 'https://www.theguardian.com/profile/' + author.replace(" ","").lower()
		content = urllib2.urlopen(url,cafile=certifi.where()).read()
		soup = BeautifulSoup(content,"lxml")
		for link in soup.find_all('a',{'data-link-name':'article'}):
			if time in link.get('href'):
				JW =link.get('href')
				if JW not in article:
					os.system("terminal-notifier -title ''\"{}\"' just published a piece' -message 'Check it now' -open \"{}\" -appIcon 'football_noti.png'".format(author,JW))
					article.append(JW)
	sleep(3600)