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

geolocator = Nominatim(user_agent="my-application", timeout=10)
Client= MongoClient('mongodb+srv://Events:0mY17NHpxeqb48ht@cluster0-fapdz.mongodb.net/main')

db= Client["events"]
hack= db.hackathons


driver = webdriver.Chrome()
driver.get("http://www.hackalist.org")
sleep(4)

des= []
image= "https://www.google.se/imgres?imgurl=https%3A%2F%2Fmedia.licdn.com%2Fmpr%2Fmpr%2Fgcrc%2Fdms%2Fimage%2FC5112AQHIotaLihFQeg%2Farticle-cover_image-shrink_600_2000%2F0%3Fe%3D2131920000%26v%3Dbeta%26t%3DVmrbbYOA3O6LC-V6mwwvZIcC1I5YfKlCgbBAHs9ihlM&imgrefurl=https%3A%2F%2Fwww.linkedin.com%2Fpulse%2Fhow-run-effective-hackathon-corporate-innovation-steve-glaveski&docid=gBhDWK77OM1UdM&tbnid=A8XEjSIId0GTAM%3A&vet=10ahUKEwiMi-ai6LfcAhXmNpoKHRQJBvEQMwjYASgCMAI..i&w=523&h=300&bih=947&biw=1920&q=hackathon&ved=0ahUKEwiMi-ai6LfcAhXmNpoKHRQJBvEQMwjYASgCMAI&iact=mrc&uact=8"
title=[]
timestamp= []
url=[]
loc=[]
gps_lat= []
gps_long= []

null = None

title= driver.find_elements_by_xpath('//h2[@class="ng-binding"]')

for x in range(len(title)):
	title.append(title[x].text)


sel= Selector(text= driver.page_source)	

location= sel.xpath('//p[@class="info-line ng-binding"]//text()').extract()

sponsor= sel.xpath('//p[@class="info-line-sm ng-binding"]//text()').extract()



for x in range(len(location)):
	loc.append(location[x].strip()[21:-1])

#for x in range(len(des)):
	#des_.append(des[x].strip())


for x in range(len(sponsor)):
	des.append(sponsor[x].strip())

"""for x in range(len(loc)):
	try:
		gps_lat.append(str(geolocator.geocode(loc[x]).latitude))
	except AttributeError:
		gps_lat.append(null)


for x in range(len(loc)):
	try:
		gps_long.append(str(geolocator.geocode(loc[x]).latitude))
	except AttributeError:
		gps_long.append(null)	"""	




ddb_data= pd.DataFrame(
    {'Image': image,
     'Title of event': title,
     'timestamp': null,
     'Location': loc,
     #'GPS_lat': gps_lat,
     #'GPS_long': gps_long,
     'Event Description': des,
     'Event URL': null
   	})

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)

driver.quit()


		




