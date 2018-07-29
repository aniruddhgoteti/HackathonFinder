import meetup.api
import json
from pymongo import MongoClient
import csv
import pandas as pd
import datetime
from datetime import datetime
from datetime import timezone

client = meetup.api.Client('')


Clt = MongoClient('')

db= Clt["events"]
hack= db.test

info= client.GetOpenEvents({'text':'hackathon'})

json_data = json.dumps(info.results, indent=5)
my_dict= json.loads(json_data)


des= []
image= []
title=[]
timestamp= []
url=[]
loc=[]
gps_lat= []
gps_long= []

null = None

for x in range(0,len(my_dict)):
	
	des.append(my_dict[x]["description"])
	title.append(my_dict[x]["group"]["name"])
	url.append(my_dict[x]["event_url"])
	timestamp.append(str(my_dict[x]["time"]+my_dict[1]["utc_offset"]))

	try:
		image.append(my_dict[x]["photo_url"])
	except KeyError:
		image.append(null)			


	try:
		loc.append(my_dict[x]["venue"]["city"] + " " + my_dict[x]["venue"]["localized_country_name"])
	except KeyError:
		loc.append(null)
	
	try:	
		gps_lat.append(str(my_dict[x]["venue"]["lat"]))
	except KeyError:
		gps_lat.append(null)

	try:	
		gps_long.append(str(my_dict[x]["venue"]["lon"]))
	except KeyError:
		gps_long.append(null)	


#print(loc_a)

db_data= pd.DataFrame(
    {'Image': image,
     'Title of event': title,
     'timestamp': timestamp,
     'Location': loc,
     'GPS_lat': gps_lat,
     'GPS_long': gps_long,
     'Event Description': des,
     'Event URL': url
   	})

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)
