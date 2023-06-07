from pymongo import MongoClient
import os
client = MongoClient(f"mongodb://localhost:27017/?retryWrites=true&w=majority")
db = client['Student_manager']
collection = db['Student']
grades_collection = db['Grade']
user_collection = db['User']
dbList = db.list_collection_names()
print(dbList)
