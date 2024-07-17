#!/usr/bin/env python

from pymongo.mongo_client import MongoClient # Import MongoClient to interact with MongoDB
from pymongo.server_api import ServerApi # Import ServerApi for server API versioning

# Define constants for MongoDB URI, database name, and collection names
ATLAS_URI = '<mongodb driver>'
DB_NAME = '<database name>'
COLL_NAME_A = '<collection name>'
COLL_NAME_R = '<collection name>'

class AtlasClient():
    def __init__ (self, altas_uri, dbname):
        self.mongodb_client = MongoClient(altas_uri) # Initialize MongoClient
        self.database = self.mongodb_client[dbname] # Access the specified database

    def ping(self):
        self.mongodb_client.admin.command('ping') # Ping the database to check the connection

    def get_collection(self, collection_name):
        collection = self.database[collection_name] # Get the specified collection
        return collection

    def find(self, collection_name, filter = {}, limit = 0):
        collection = self.database[collection_name] # Get the specified collection
        items = list(collection.find(filter=filter, limit=limit)) # Find documents with optional filter and limit
        return items

    def drop_all_documents(self, collection_name):
        collection = self.database[collection_name] # Get the specified collection
        del_docs = collection.delete_many({}) # Delete all documents in the collection
        print(f"Deleted {del_docs.deleted_count} documents from the {collection_name} collection")

# Initialize AtlasClient with MongoDB URI and database name
atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
register = atlas_client.get_collection(COLL_NAME_R) # Get the registration collection
attendance = atlas_client.get_collection(COLL_NAME_A) # Get the attendance collection

def registerStudents(name,usn,image): # Function to register students
    StudentDete = {"name": name, "usn": usn, "img_path": image} # Create a student document
    try:
        register.insert_one(StudentDete) # Insert the student document into the registration collection
        print("Registered Student")
    except:
        print("Error Occured") # Print error message if insertion fails

def takeAttendance(date,time,name,usn): # Function to take attendance
    AttendanceDete = {"date": date, "time": time, "name": name, "usn": usn} # Create an attendance document
    try:
        attendance.insert_one(AttendanceDete) # Insert the attendance document into the attendance collection
        print("Attendance Marked")
    except:
        print("Error Occured") # Print error message if insertion fails

def dropDocs(): # Drop the documents in the collections
    coll_names = [COLL_NAME_A, COLL_NAME_R]
    for coll_to_drp in coll_names:
        atlas_client.drop_all_documents(coll_to_drp)

def listPath(): # Get the image path stored the database
    mylist = []
    for images in register.find({},{"_id": 0, "img_path": 1}): # Find all image paths in the registration collection
        path = images.values()
        for images in path:
            mylist.append(images) # Add each image path to the list
    return mylist

def check_A(): # Check the collection attendance for the existing names
    name_a = []
    for names_a in attendance.find({},{"_id": 0, "name": 1}): # Find all names in the attendance collection
        nameV_a = names_a.values()
        for nameS_a in nameV_a:
            name_a.append(nameS_a) # Add each name to the list
    return name_a

def check_R(): # Check the collection registration for the existing names
    name_r = []
    for names_r in register.find({},{"_id": 0, "name": 1}): # Find all names in the registration collection
        nameV_r = names_r.values()
        for nameS_r in nameV_r:
            name_r.append(nameS_r) # Add each name to the list
    return name_r
