from pymongo import MongoClient
import os
import dotenv as env

env.load_dotenv()

uri = os.getenv("uri")
client = MongoClient(uri)


for db_name in client.list_database_names():
    print(db_name)

client.close()