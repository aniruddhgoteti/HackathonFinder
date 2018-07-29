import meetup.api
import json
from pymongo import MongoClient
import csv
import pandas as pd

client = meetup.api.Client('')


Clt= MongoClient('localhost', 27017)
db= Clt["hackathons"]
hack= db.hack_finder

info= client.GetOpenEvents({'text':'hackathon'})

json_data = json.dumps(info.results, indent=5)
my_dict= json.loads(json_data)


des= []
title=[]
url=[]
loc=[]
gps= []

null = None

for x in range(0,len(my_dict)-1):
	des.append(my_dict[x]["description"])
	title.append(my_dict[x]["group"]["name"])
	url.append(my_dict[x]["event_url"])

	try:
		loc.append(my_dict[x]["venue"]["city"] + " " + my_dict[x]["venue"]["localized_country_name"])
	except KeyError:
		loc.append(null)
	
	try:	
		gps.append(str(my_dict[x]["venue"]["lat"]) + ","+ str(my_dict[x]["venue"]["lon"]))
	except KeyError:
		gps.append(null)


#print(loc_a)

db_data= pd.DataFrame(
    {'Title of event': title,
     'Location': loc,
     'GPS': gps,
     'Event Description': des,
     'Event URL': url
   	})

records = json.loads(db_data.T.to_json()).values()
hack.insert(records)
