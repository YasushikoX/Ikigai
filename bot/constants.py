import json

from pymongo import MongoClient # Use this library to interact with pymongo


with open("config.json", "r") as file:
    config = json.loads(open('config.json').read())

TOKEN = config['token']
# DB_TOKEN = config['db_token']

DB_TOKEN = config['mongodb']


CLUSTER = MongoClient(DB_TOKEN) # Only define this once
GROUP = CLUSTER["Ikigai"] # replace group with whatever you called your heading of collectionss

collection = GROUP["user-info"] # This is a section of your database you can add/remove stuff to/from