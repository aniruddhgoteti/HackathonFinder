from eventbrite import Eventbrite
import json
from pymongo import MongoClient
import csv
import pandas as pd
import sys, getopt, pprint
import datetime
from operator import add
from geopy.geocoders import Nominatim

geolocator = Nominatim()


Client= MongoClient('localhost', 27017)
db= Client["hackathons"]
hack= db.hack_finder


eventbrite = Eventbrite('XKPWE63CH4NCOT6C7OAY')

data= dict(q='hackathons')

hackathons = eventbrite.get('/events/search', data=data)

json_data = json.dumps(hackathons, indent=5)
my_dict= json.loads(json_data)

title=[]
for each in my_dict["events"]:
	title.append(each["name"]["text"])

#print(title)	

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

start_time=[]
start_date=[]
end_time= []
end_date= []
null = None

for x in end_time_date:
	end_date.append(x[0:10])
	end_time.append(x[11:19])

for x in start_time_date:
	start_date.append(x[0:10])
	start_time.append(x[11:19])


for x in range(len(end_date)):
	d = datetime.datetime.strptime(end_date[x], '%Y-%m-%d')
	end_date[x]=  d.strftime('%d/%b/%Y')

#print(end_date)

for x in range(len(start_date)):
	d = datetime.datetime.strptime(start_date[x], '%Y-%m-%d')
	start_date[x]=  d.strftime('%d/%b/%Y')

#print(start_date)		

date= []
date=list( map(str.__add__, start_date, end_date) )

for x in range(len(date)):
	date[x]= date[x][0:11]+ "-" + date[x][11:22]

#print(date)	

time= []
time=list( map(str.__add__, start_time, end_time) )

for x in range(len(time)):
	time[x]= time[x][0:8]+ "-" + time[x][8:17]

#print(time)

loc=[]
for each in my_dict["events"]:
	loc.append(each["start"]["timezone"])

#print(loc)	

gps= []
for x in range(len(loc)):
	if loc[x]=="America/Sao_Paulo":
		loc[x]= "America"
	gps.append(str(geolocator.geocode(loc[x]).latitude)+ "," + str(geolocator.geocode(loc[x]).longitude))

#print(gps)   


des= []
for each in my_dict["events"]:
	des.append(each["description"]["html"])

#print(des)	



db_data= pd.DataFrame(
    {'Image': null,
     'Title of event': title,
     'Date': date,
     'Time': time,
     'Location': loc,
     'GPS': gps,
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








