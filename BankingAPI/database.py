from pymongo import MongoClient

MONGO_URL = "mongodb+srv://grovesrpg:Atletico111!@citidb.feyqcz0.mongodb.net/?appName=CitiDB"

client = MongoClient(MONGO_URL)

db = client["banking_api"]

customers_collection = db["customers"]
accounts_collection = db["accounts"]
counters_collection = db["counters"]