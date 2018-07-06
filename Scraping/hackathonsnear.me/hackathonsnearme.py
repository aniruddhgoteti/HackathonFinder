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
driver.get("http://hackathonsnear.me/")
sleep(4)

title_ = []
dates_= []
loc_= []
gps_ = []
url_=[]
null = None

title= driver.find_elements_by_xpath('//a[@class="hackathon-name ng-binding"]')


sel= Selector(text= driver.page_source)	
dates= sel.xpath('//div[@class="columns small-3 medium-2 large-3 ng-binding"]//text()').extract()

extract_url=sel.xpath('//a/@href').extract()

url= list(OrderedDict.fromkeys(extract_url))
#url_=url[4:-4]
url_= url[4:-4]

location= sel.xpath('//div[@class="columns small-4 medium-3 large-2 ng-binding"]//text()').extract()

for x in range(len(title)):
	title_.append(title[x].text)
	dates_.append(dates[x].strip())


for x in range(len(location)):
	if len(location[x].strip())>6:
		loc_.append(location[x].strip())
	
for x in range(len(loc_)):
	try:
		gps_.append(str(geolocator.geocode(loc_[x]).latitude)+ "," + str(geolocator.geocode(loc_[x]).longitude))
	except AttributeError:
		gps_.append(null)
	

title_ = list(OrderedDict.fromkeys(title_))
#list(set(title_))	

dates_ = list(OrderedDict.fromkeys(dates_))
#list(set(dates_))
		

print(len(title_), len(dates_), len(loc_), len(gps_), len(url_))
print(url_)
print(title_)


db_data= pd.DataFrame(
    {'Image': null,
     'Title of event': title_,
     'Date': dates_,
     'Time': null,
     'Location': loc_,
     'GPS': gps_,
     'Event Description': null,
     'Event URL': url_
    })

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)

driver.quit()
