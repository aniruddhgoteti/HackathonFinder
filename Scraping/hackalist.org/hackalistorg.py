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

geolocator = Nominatim()
Client= MongoClient('localhost', 27017)
db= Client["hackathons"]

hack= db.hack_finder


driver = webdriver.Chrome()
driver.get("http://www.hackalist.org")
sleep(4)

title_ = []
dates_= []
loc_= []
gps_ = []
url_=[]
sponsor_= []

null = None

title= driver.find_elements_by_xpath('//h2[@class="ng-binding"]')

for x in range(len(title)):
	title_.append(title[x].text)


sel= Selector(text= driver.page_source)	

location= sel.xpath('//p[@class="info-line ng-binding"]//text()').extract()

sponsor= sel.xpath('//p[@class="info-line-sm ng-binding"]//text()').extract()



for x in range(len(location)):
	loc_.append(location[x].strip()[21:-1])

#for x in range(len(des)):
#	des_.append(des[x].strip())


for x in range(len(sponsor)):
	sponsor_.append(sponsor[x].strip())

for x in range(len(loc_)):
	try:
		gps_.append(str(geolocator.geocode(loc_[x]).latitude)+ "," + str(geolocator.geocode(loc_[x]).longitude))
	except AttributeError:
		gps_.append(null)



url= sel.xpath('//a/@href').extract()

url_.append(url[5])
url_.append(url[6])
url_.append(url[9])
url_.append(url[12])
url_.append(url[-5])
url_.append(url[-1])

db_data= pd.DataFrame(
    {'Image': null,
     'Title of event': title_,
     'Date': null,
     'Time': null,
     'Location': loc_,
     'GPS': gps_,
     'Event Description': null,
     'sponsor': sponsor_,
     'Event URL': url_
    })

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)

driver.quit()


		




