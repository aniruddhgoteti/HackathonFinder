from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify

app= Flask(__name__)

app.config['MONGO_DBNAME'] = 'hackathons'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hackathons'

mongo=PyMongo(app)


@app.route('/list')

def printList():
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


if __name__=='__main__':
	app.run(debug=True)
