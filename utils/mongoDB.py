import json
import pymongo


def connectToMongo(atlas_link, databaseName):
    client = pymongo.MongoClient(atlas_link, socketTimeoutMS=5000, serverSelectionTimeoutMS=5000)
    print("database connected...")
    return client[databaseName]


class DataBaseUtility:
    def __init__(self, atlas_link, databaseName):
        self.db = connectToMongo(atlas_link=atlas_link, databaseName=databaseName)

    def login(self, username, password):
        print("in login")
        allUsers = self.db['users-login'].find({"username": username, "password": password})
        print(allUsers)
        userExist = None
        for i in allUsers:
            userExist = i

        if userExist is None:
            return {'userExist': False}
        else:
            return {'userExist': True }
