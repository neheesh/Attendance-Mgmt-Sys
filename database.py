#!/usr/bin/env python

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

ATLAS_URI = '<uri>'
DB_NAME = '<database_name>' #assign the database name
COLL_NAME_A = '<collection_name_which_stores_attendance>' #assign the collection name for attendance
COLL_NAME_R = '<collection_name_which_stores_registration>' #assign the collection name for registration

class AtlasClient():
    def __init__ (self, altas_uri, dbname): #initialize the database
        self.mongodb_client = MongoClient(altas_uri)
        self.database = self.mongodb_client[dbname]

    def ping(self): #pings the database
        self.mongodb_client.admin.command('ping')

    def get_collection(self, collection_name): #get the names for the collection in the database
        collection = self.database[collection_name]
        return collection

    def find(self, collection_name, filter = {}, limit = 0): #find the documents in the collection
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items

    def drop_all_documents(self, collection_name):
        collection = self.database[collection_name]
        del_docs = collection.delete_many({})
        print(f"Deleted {del_docs.deleted_count} documents from the {collection_name} collection")

atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
register = atlas_client.get_collection(COLL_NAME_R)
attendance = atlas_client.get_collection(COLL_NAME_A)

def registerStudents(name,usn,image): #function to register students
    StudentDete = {"name": name, "usn": usn, "img_path": image}
    try:
        register.insert_one(StudentDete)
        print("Registered Student")
    except:
        print("Error Occured")

def takeAttendance(date,time,name,usn): #function to take attendance
    AttendanceDete = {"date": date, "time": time, "name": name, "usn": usn}
    try:
        attendance.insert_one(AttendanceDete)
        print("Attendance Marked")
    except:
        print("Error Occured")

def listPath(): #get the image path stored the database
    mylist = []
    for images in register.find({},{"_id": 0, "img_path": 1}):
        path = images.values()
        for images in path:
            mylist.append(images)
    return mylist

def check_A(): #check the collection attendance for the existing names
    name_a = []
    for names_a in attendance.find({},{"_id": 0, "name": 1}):
        nameV_a = names_a.values()
        for nameS_a in nameV_a:
            name_a.append(nameS_a)
    return name_a

def check_R(): #check the collection registration for the existing names
    name_r = []
    for names_r in register.find({},{"_id": 0, "name": 1}):
        nameV_r = names_r.values()
        for nameS_r in nameV_r:
            name_r.append(nameS_r)
    return name_r
