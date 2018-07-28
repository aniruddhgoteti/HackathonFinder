
import pymongo


client = pymongo.MongoClient('mongodb+srv://Events:0mY17NHpxeqb48ht@cluster0-fapdz.mongodb.net/main')
db = client["events"]
collection = db.test

collection.create_index([('Event Description', pymongo.TEXT)], name='search_index', default_language='english')

search_this_string = "hackathon"

a=[]
a =collection.find({"$text": {"$search": search_this_string}})
db.hackathons.insert(a)
