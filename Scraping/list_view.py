import future as f
import feedparser
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask import jsonify
import pandas as pd
import os
import pandas as pd
import numpy as np
from IPython.core.display import display, HTML
import pymongo
from pymongo import MongoClient
from pymongo import DeleteMany
import folium
from werkzeug.contrib.atom import AtomFeed
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from folium import IFrame
import base64

from threading import *
import copy

class Future:

    def __init__(self,func,*param):
        # Constructor
        self.__done=0
        self.__result=None
        self.__status='working'

        self.__C=Condition()   # Notify on this Condition when result is ready

        # Run the actual function in a separate thread
        self.__T=Thread(target=self.Wrapper,args=(func,param))
        self.__T.setName("FutureThread")
        self.__T.start()

    def __repr__(self):
        return '<Future at '+hex(id(self))+':'+self.__status+'>'

    def __call__(self):
        self.__C.acquire()
        while self.__done==0:
            self.__C.wait()
        self.__C.release()
        # We deepcopy __result to prevent accidental tampering with it.
        a=copy.deepcopy(self.__result)
        return a

    def Wrapper(self, func, param):
        # Run the actual function, and let us housekeep around it
        self.__C.acquire()
        try:
            self.__result=func(*param)
        except:
            self.__result="Exception raised within Future"
        self.__done=1
        self.__status='self.__result'
        self.__C.notify()
        self.__C.release()




Client= MongoClient('localhost', 27017)
db= Client["hackathons"]

hack= db.hack_finder

app= Flask(__name__)

app.config['MONGO_DBNAME'] = 'hackathons'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hackathons'

api = Api(app)

mongo=PyMongo(app)

@app.route('/list')
def getList():
	
	list=mongo.db.hack_finder
	list_find= list.find()
	result= []

	for j in list_find:
		result.append({'Title of event': j['Title of event'],
    	# 'Date': j['Date'],
    	# 'Time': j['Time'],
     	'Location': j['Location'],
     	'GPS': j['GPS'],
    	# 'Event Description': j['Event Description'],
     	'Event URL': j['Event URL']})

	return jsonify(result)	


@app.route('/map')
def getmap():
	with app.app_context():
		global hackmap
		list=mongo.db.hack_finder
		list_find= list.find()
		result= []
		gps_= []
		null= None

		for j in list_find:
			result.append({'Title of event': j['Title of event'],
    		# 'Date': j['Date'],
    		# 'Time': j['Time'],
     		'Location': j['Location'],
     		'GPS': j['GPS'],
    		# 'Event Description': j['Event Description'],
     		'Event URL': j['Event URL']})
	
	
		for x in range(len(result)):
			try:
		
				if type(result[x]["GPS"][0])== float:
					gps_.append(str(result[x]["GPS"][0])+","+str(result[x]["GPS"][1]))
				else:
					gps_.append(result[x]["GPS"])
				
			except TypeError:
				gps_.append(None)
				


		
		gps_ = pd.Series(gps_)		


		df1 = pd.DataFrame(result)
		df1.drop(['GPS'], axis=1)
		df1['GPS'] = gps_.values

		Lat= []
		Long=[]
		Labels= []
		url= []

		for x in range(len(df1)):
			try:
				Lat.append(float(df1.GPS[x].split(',')[0][0:7]))
				Long.append(float(df1.GPS[x].split(',')[1][0:7]))
				Labels.append("Title= " + df1["Title of event"][x])
				url.append("URL=" + df1["Event URL"][x])
			except AttributeError:
				pass

		Lat = pd.Series(Lat)
		Long= pd.Series(Long)

		df = pd.DataFrame()
		df["Lat"]= Lat.values
		df["Long"]= Long.values

		resolution, width, height = 75, 7, 3
		encoded = base64.b64encode(open('images.png', 'rb').read()).decode()

		
		locationlist = df[["Lat","Long"]].values.tolist()

		hackmap = folium.Map(location=[35, 100],tiles='Stamen Toner', zoom_start=14)
		for point in range(len(locationlist)):
			html = '<img src="data:image/png;base64,{}">'.format
			iframe = IFrame(html(encoded)+ Labels[point]+ " " +  url[point], width=(width*resolution)+20, height=(height*resolution)+20)
			icon = folium.Icon(color="red", icon="ok")
			popup = folium.Popup(iframe, max_width=2650)
			folium.Marker(locationlist[point], popup=popup).add_to(hackmap)
		

		return hackmap.get_root().render()

		#hackmap.save('newmap.html')

		#return app.send_static_file('newmap.html')
  #Labels[point], parse_html=True,

@app.route('/feed')
def getfeed():
	hit_list = [ "https://devpost.com/hackathons.rss", "https://disruptorshandbook.com/feed", "https://startup-calendar.com/hackathons/feed/", "https://www.meetup.com/events/rss/191381583/35ae41e956b41b34348dc8a1ff030c6947d7bc13/going" ] # list of feeds to pull down

	future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]

	feeds = [future_obj() for future_obj in future_calls]

	entries = []
	for feed in feeds:
		entries.extend( feed[ "items" ] )


	return jsonify(entries)	

	



#api.add_resource(HackathonList, '/list') # Route_1
#api.add_resource(Map, '/map') # Route_2
#api.add_resource(Feed, '/feed') # Route_3

if __name__=='__main__':
	
	app.run(debug=True)
