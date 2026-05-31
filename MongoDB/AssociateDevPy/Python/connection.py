from pymongo import MongoClient

uri = "mongodb+srv://Admin:Vk06Ej8FroxNbzgR@education.1h51hgs.mongodb.net/?appName=Education"


client = MongoClient(uri)


for db_name in client.list_database_names():
    print(db_name)

client.close()