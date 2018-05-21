import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import certifi
from datetime import datetime
import os
import pdb

def notify(piece,author_name):
	os.system("/usr/local/bin/terminal-notifier -title ''\"{}\"' just published a piece' -message 'Check it now' -open \"{}\" -appIcon '/Users/venkateshs/Desktop/Personal/Football/football_noti.png'".format(author_name,piece))

def url_creation(author):
	if author == 'Rory Smith':
		url = 'https://www.nytimes.com/column/on-soccer'
	else:
		url = 'https://www.theguardian.com/profile/' + author
	return (url,author)


def soup_creation(url_author):
	content = urllib2.urlopen(url_author[0],cafile=certifi.where()).read()
	soup = BeautifulSoup(content,"lxml")
	if 'guardian' in url_author[0]:
		soup = soup.find_all('a',{'data-link-name':'article'})
	else:
		soup = soup.find_all('a',class_ = 'story-link')
	return (soup,url_author[1])

def content_extraction(content):
	global article
	year = datetime.now().strftime('%Y')
	day = '21'
	piece = content[0][0].get('href')

	if 'guardian' in piece:
		month = datetime.now().strftime('%b').lower()
		time = ('/').join([year,month,day])
		if time in piece:
			if piece not in article:
				article.append(piece)
				author_name = content[1]
				piece = content[0][0].get('href')
				notify(piece,author_name)


	elif 'nytimes' in piece:
		month = datetime.now().strftime('%m')
		time = ('/').join([year,month,day])
		if time in piece:
			if piece not in article:
				article.append(piece)
				piece = content[0][0].get('href')
				author_name = content[1]
				notify(piece,author_name)







article = []
authors = ['jonathanwilson','sidlowe','danieltaylor','sachinnakrani','amylawrence','barneyronay','Rory Smith']
while True:
	print 'Next'
	map(content_extraction,map(soup_creation,map(url_creation,authors)))
	sleep(3600)
