from pymongo import MongoClient


MONGO_URI = MongoClient('localhost', 27017)
DB = MONGO_URI['wallet']
mongo = DB.card