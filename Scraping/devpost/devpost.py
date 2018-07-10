from time import sleep
from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from collections import OrderedDict
import pandas as pd
import json
from itertools import repeat

from geopy.geocoders import Nominatim


Client= MongoClient('localhost', 27017)
db= Client["hackathons"]

hack= db.hack_finder

driver = webdriver.Chrome()
driver.get("https://devpost.com/hackathons")
sleep(4)

title_ = []
dates_= []
loc_= []
gps_ = []
url_=[]
prizes_= []
des_= []
image_=[]

null = None


title = driver.find_elements_by_xpath('//h2[@class="title"]')

for x in range(len(title)):
	title_.append(title[x].text)


des = driver.find_elements_by_xpath('//p[@class="challenge-description"]')	

for x in range(len(des)):
	des_.append(des[x].text)


loc= driver.find_elements_by_xpath('//p[@class="challenge-location"]')	

for x in range(len(loc)):
	loc_.append(loc[x].text)

geolocator = Nominatim()

for x in range(len(loc_)):
	try:
		gps_.append(str(geolocator.geocode(loc_[x]).latitude)+ "," + str(geolocator.geocode(loc_[x]).longitude))
	except AttributeError:
		gps_.append(null)


#date= driver.find_elements_by_xpath('//div[@class="small-10 large-9 columns"]//span[@class="value date-range"]')
#for x in range(len(date)):
#	dates_.append(date[x].text.strip()[4:6]+ "/" + date[x].text.strip()[0:3]+ "/" + date[x].text.strip()[13:17] + "-" +date[x].text.strip()[9:11] + "/" + date[x].text.strip()[0:3]+ "/" + date[x].text.strip()[13:17])


prizes=  driver.find_elements_by_xpath('//span[@class="value"]')

for x in range(len(prizes)):
	prizes_.append(prizes[x].text)


for image in driver.find_elements_by_xpath('//div[@class="results"]//img[@src]'):
	image_.append(image.get_attribute('src'))


for url in driver.find_elements_by_xpath('//div[@class="results"]//a[@href]'):
	url_.append(url.get_attribute('href'))

print(len(title_), len(url_), len(gps_), len(des_), len(prizes_), len(image_), len(loc_))
print(title_)
print(url_)

print(prizes_)

#sel= Selector(text= driver.page_source)	
"""
db_data= pd.DataFrame(
    {'Image': image_,
     'Title of event': title_,
     'Date': dates_,
     'Time': null,
     'Location': title_,
     'GPS': gps_,
     'Event Description': des_,
     'sponsor': null,
     'Event URL': url_
    })

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)

driver.quit() """