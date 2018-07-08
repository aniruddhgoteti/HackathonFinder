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
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

api = Api(app)

Client= MongoClient('localhost', 27017)
db= Client["hackathons"]

hack= db.hack_finder

app= Flask(__name__)

app.config['MONGO_DBNAME'] = 'hackathons'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hackathons'

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

		for x in range(len(df1)):
			try:
				Lat.append(float(df1.GPS[x].split(',')[0][0:5]))
				Long.append(float(df1.GPS[x].split(',')[1][0:5]))
				Labels.append(df1["Title of event"][x])
			except AttributeError:
				pass

		Lat = pd.Series(Lat)
		Long= pd.Series(Long)

		df = pd.DataFrame()
		df["Lat"]= Lat.values
		df["Long"]= Long.values

		locationlist = df[["Lat","Long"]].values.tolist()

		hackmap = folium.Map(location=[35, 100],tiles='Stamen Toner', zoom_start=14)
		for point in range(len(locationlist)):
			popup = folium.Popup(Labels[point], parse_html=True)
			folium.Marker(locationlist[point], popup=popup).add_to(hackmap)
		

		return hackmap.get_root().render()

		#hackmap.save('newmap.html')

		#return app.send_static_file('newmap.html')
  


#api.add_resource(HackathonList, '/list') # Route_1
#api.add_resource(Map, '/map') # Route_2
#api.add_resource(Calemdar, '/cal') # Route_3
#api.add_resource(Feed, '/feed') # Route_3

if __name__=='__main__':
	
	app.run(debug=True)
