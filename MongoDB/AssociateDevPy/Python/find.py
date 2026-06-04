from pymongo import MongoClient
import os
import dotenv as env
import pprint

env.load_dotenv()
uri = os.getenv("uri")


client = MongoClient(uri)
db = client.sample_mflix
movies = db.movies


find = movies.find().limit(5)
findOne = movies.find_one({'name':'Mariana'})
updateMany = movies.update_many({},{ '$set':{'balance':0} })
cursor = movies.find({'genres': {'$in': ['Comedy']}}).limit(5)
docs = 0
"""
for document in find :
    docs+= 1
    pprint.pprint(document)
    print(f'Docs found: {docs}')"""

for document in cursor:
    pprint.pprint(document["title"])


client.close()