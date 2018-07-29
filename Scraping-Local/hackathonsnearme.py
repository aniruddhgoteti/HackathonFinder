from time import sleep
from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from collections import OrderedDict
import pandas as pd
import json
from itertools import repeat
import datetime
from datetime import datetime
from datetime import timezone
from time import time
from geopy.geocoders import GoogleV3

key= ""
geolocator = GoogleV3(api_key=key, timeout=10)


Client= MongoClient('')
db= Client["events"]
hack= db.hackathons



driver = webdriver.Chrome()
driver.get("http://hackathonsnear.me/")
sleep(4)

title_ = []
dates_= []
loc_= []
gps_lat = []
gps_long= []
url_= []

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
		gps_lat.append(str(geolocator.geocode(loc_[x]).latitude))
	
	except AttributeError:
		gps_lat.append(null)

for x in range(len(loc_)):
	try:
		gps_long.append(str(geolocator.geocode(loc_[x]).longitude))
		
	except AttributeError:
		gps_long.append(null)	
	

title_ = list(OrderedDict.fromkeys(title_))
#list(set(title_))	
start_time_date=[]
unix_start= []

dates_ = list(OrderedDict.fromkeys(dates_))
for x in range(len(dates_)):
	try:
		start_time_date.append(dates_[x].split('-')[0].strip() + " 2018")
		dt = datetime.strptime(start_time_date[x], '%b %d %Y')
		timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
		unix_start.append(timestamp)
	except ValueError:
		unix_start.append(null)
		
#dt = datetime.strptime(start_time_date[x], '%Y-%m-%dT%XZ')

#list(set(dates_))
timestamp=[]

for x in range(len(unix_start)):
	timestamp.append(str(unix_start[x]) + "," + str(unix_start[x]))		

print(len(title_), len(dates_), len(loc_),  len(url_))
print(url_)
print(title_)
print(timestamp)

db_data= pd.DataFrame(
    {'Image': "https://www.google.se/imgres?imgurl=http%3A%2F%2Fco-station.com%2Fwp-content%2Fuploads%2F2017%2F05%2Fhackathon-graphic.png&imgrefurl=http%3A%2F%2Fco-station.com%2F2017%2F05%2F02%2F5-reasons-join-hackathon%2F&docid=ShALBLAg56sXnM&tbnid=Ej3Flrbkew4bQM%3A&vet=10ahUKEwjuwL6qwKbcAhUCYZoKHRBLCS8QMwjcASgGMAY..i&w=700&h=300&bih=947&biw=1920&q=hackathon&ved=0ahUKEwjuwL6qwKbcAhUCYZoKHRBLCS8QMwjcASgGMAY&iact=mrc&uact=8",
     'Title of event': title_,
     'timestamp': timestamp,
     'Location': loc_,
     'GPS_lat': gps_lat,
     'GPS_long': gps_long,
     'Event Description': null,
     'Event URL': url_
    })

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)

driver.quit()
