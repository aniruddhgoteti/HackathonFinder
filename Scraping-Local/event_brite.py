from eventbrite import Eventbrite
import json
from pymongo import MongoClient
import csv
import pandas as pd
import sys, getopt, pprint
import datetime
from datetime import datetime
from datetime import timezone
from operator import add
from geopy.geocoders import GoogleV3

key= ""

geolocator = GoogleV3(api_key=key,user_agent="my-application", timeout=10)


Client = MongoClient('')

db= Client["events"]
hack= db.hackathons


eventbrite = Eventbrite('XKPWE63CH4NCOT6C7OAY') #PersonalAPI

data= dict(q='hackathons')

hackathons = eventbrite.get('/events/search', data=data)

json_data = json.dumps(hackathons, indent=5)
my_dict= json.loads(json_data)

title=[]
for each in my_dict["events"]:
	title.append(each["name"]["text"])

#print(title)	

image= []
for x in range(len(title)):
	try:
		image.append(my_dict["events"][x]["logo"]["original"]["url"])
	except TypeError:
		image.append("N/A")

url= []
for each in my_dict["events"]:
	url.append(each["url"])

#print(url)

start_time_date= []
for each in my_dict["events"]:
	start_time_date.append(each["start"]["utc"])

#print(start_time_date)

end_time_date= []
for each in my_dict["events"]:
	end_time_date.append(each["end"]["utc"])

#print(end_time_date)

unix_start= []
for x in range(len(start_time_date)):
	dt = datetime.strptime(start_time_date[x], '%Y-%m-%dT%XZ')
	timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
	unix_start.append(timestamp)

unix_end= []
for x in range(len(end_time_date)):
	dt = datetime.strptime(end_time_date[x], '%Y-%m-%dT%XZ')
	timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
	unix_end.append(timestamp)


timestamp= []

for x in range(len(end_time_date)):
	timestamp.append(str(unix_start[x]) + "," + str(unix_end[x]))

loc=[]
for each in my_dict["events"]:
		loc.append(each["start"]["timezone"])

print(loc)	


gps_lat= []
for x in range(len(loc)):
	if loc[x]=="America/Sao_Paulo":
		loc[x]= "America"
	gps_lat.append(str(geolocator.geocode(loc[x]).latitude))

#print(gps)   

gps_long= []
for x in range(len(loc)):
	if loc[x]=="America/Sao_Paulo":
		loc[x]= "America"
	gps_long.append(str(geolocator.geocode(loc[x]).longitude))




des= []
for each in my_dict["events"]:
	des.append(each["description"]["html"])

#print(des)	



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
#hack.insert_many(db_data.to_dict())

"""hack_data = { 
'Image':"N/A",

'Title of event': title,

'Date': "N/A",
'Time': "N/A",
'Location': "Online",
'GPS': "N/A",
'Event Description': "N/A",
'Prizes': "N/A",
'Schedule': "N/A",
'Sponsor': "N/A",
'Event URL': "null",
}

result= hack.insert(hack_data)"""








