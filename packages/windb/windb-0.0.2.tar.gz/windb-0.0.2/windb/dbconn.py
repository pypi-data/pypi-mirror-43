from pymongo import MongoClient

MONGO_CLIENT: MongoClient = None

def init(host='localhost', port=27017, **kwargs):
    global MONGO_CLIENT
    MONGO_CLIENT = MongoClient(host=host, port=port, **kwargs)

def db(name):
    return MONGO_CLIENT[name]
