import pymongo
from pymongo import MongoClient
client=MongoClient("mongodb+srv://analytics:analytics-password@cluster0.labxu.mongodb.net/Ipl?retryWrites=true&w=majority")

def get_client():
    return client


        
    