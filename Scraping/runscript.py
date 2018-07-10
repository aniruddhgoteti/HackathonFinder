import os
import pymongo
from pymongo import MongoClient
from pymongo import DeleteMany, DeleteOne
from flask_pymongo import PyMongo
from time import sleep

#Run multiple feeds

os.system (r"python C:\Users\aniru\OneDrive\Documents\GitHub\HackathonFinder\Scraping\event_brite\event_brite.py")
sleep(3)
os.system (r"python C:\Users\aniru\OneDrive\Documents\GitHub\HackathonFinder\Scraping\hackalist.org\hackalistorg.py")
sleep(3)

os.system (r"python C:\Users\aniru\OneDrive\Documents\GitHub\HackathonFinder\Scraping\hackathonsnear.me\hackathonsnearme.py")
sleep(3)

os.system (r"python C:\Users\aniru\OneDrive\Documents\GitHub\HackathonFinder\Scraping\hackevents.co\hackevents\hackevents\spiders\hack.py")
sleep(3)
os.system (r"python C:\Users\aniru\OneDrive\Documents\GitHub\HackathonFinder\Scraping\meetup\meet_up.py")
sleep(3)
os.system (r"python C:\Users\aniru\OneDrive\Documents\GitHub\HackathonFinder\Scraping\postscapes\postscapes.py")
sleep(3)

Client= MongoClient('localhost', 27017)
db= Client["hackathons"]

hack= db.hack_finder


# Delete duplicate values

cursor = hack.aggregate(
    [
        {"$group": {"_id": "$Title of event", "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": { "$gte": 2 }}}
    ]
)

response = []
for doc in cursor:
    del doc["unique_ids"][0]
    for id in doc["unique_ids"]:
        response.append(id)

hack.remove({"_id": {"$in": response}})
sleep(10)