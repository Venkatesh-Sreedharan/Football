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
article = []

while True:
	# time = ('/').join([year,month,day])
	# for author in ['Jonathan Wilson','Sid Lowe','Daniel Taylor','Sachin Nakrani','Amy Lawrence','Barney Ronay']:
	# 	print author
	# 	url = 'https://www.theguardian.com/profile/' + author.replace(" ","").lower()
	# 	content = urllib2.urlopen(url,cafile=certifi.where()).read()
	# 	soup = BeautifulSoup(content,"lxml")
	# 	for link in soup.find_all('a',{'data-link-name':'article'}):
	# 		if time in link.get('href'):
	# 			JW =link.get('href')
	# 			if JW not in article:
	# 				os.system("terminal-notifier -title ''\"{}\"' just published a piece' -message 'Check it now' -open \"{}\" -appIcon 'football_noti.png'".format(author,JW))
	# 				article.append(JW)				
	author = 'Rory Smith'
	month = datetime.now().strftime('%m')
	time = ('/').join([year,month,day])
	url = 'https://www.nytimes.com/column/on-soccer'
	content = urllib2.urlopen(url,cafile=certifi.where()).read()
	soup = BeautifulSoup(content,"lxml")
	for link in soup.find_all('a', class_= 'story-link'):
		if time in link.get('href') and author.upper() in link.find_all('p',class_='byline')[0].get_text():
			JW = link.get('href')
			if JW not in article:
				os.system("terminal-notifier -title ''\"{}\"' just published a piece' -message 'Check it now' -open \"{}\" -appIcon 'football_noti.png'".format(author,JW))
				article.append(JW)
	sleep(3600)


