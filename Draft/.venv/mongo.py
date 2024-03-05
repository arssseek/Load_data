from pymongo import MongoClient
import pandas as pd
import time

hostname = 'localhost'
port = 27023
username = "Test"
password = "mongo_Test"

client = MongoClient(hostname, port, username=username, password=password)
current = client["Test"]
collections = current["employees"]

keys = ['email','inactive','login','name']
values_dict = {key: [] for key in keys}
for doc in collections.find():
    values_dict[keys[0]].append(doc.get('email'))
    values_dict[keys[1]].append(doc.get('inactive'))
    values_dict[keys[2]].append(doc.get('login'))
    values_dict[keys[3]].append(doc.get('name'))
df = pd.DataFrame(values_dict)
print(df.values)