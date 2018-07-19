from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import json
from pymongo import MongoClient
import csv
import pandas as pd
import sys, getopt, pprint
import datetime
import pymongo
from pymongo import MongoClient
from pymongo import DeleteMany

Client = MongoClient('mongodb+srv://Events:0mY17NHpxeqb48ht@cluster0-fapdz.mongodb.net/main')

db= Client["events"]
hack= db.hackathons

list_find= hack.find()
result= []


 # Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
     flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
     creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
 
 # Call the Calendar API

now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                       maxResults=10, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])
 
if not events:
     print('No upcoming events found.')
for event in events:
     start = event['start'].get('dateTime', event['start'].get('date'))
     print(start, event['Title'])
 
# =============================================================================
# Iterating through array to make event body for each object
# =============================================================================
for event in list_find:
#dictionary = json.loads(eventsDataframe.to_json(orient='records'))
#for event in dictionary:      
	try:
		eventToInsert = {
            	'Title': event['Title of event'],
           		'location': event['Location'],
            	'description': event['Event Description'],
            	'start': {
                	    'dateTime': event['timestamp'],
                    	'timeZone': 'Europe/Copenhagen'
                    	}
            	}
	except KeyError:
		pass
eventToInsert = service.events().insert(calendarId='valuer.ai_ena2qmu18igpl0pagtk5p31toc@group.calendar.google.com', body=eventToInsert).execute()