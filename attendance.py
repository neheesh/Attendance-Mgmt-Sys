#!/usr/bin/env python

import cv2 # OpenCV for image processing
import face_recognition # Face recognition library
import os # Operating system interface
import numpy as np # Numerical operations
import re # Regular expressions
from datetime import datetime # Date and time handling
import requests as rq # HTTP requests

# Import custom database functions
from database import takeAttendance, listPath, check_A, check_R

def AttFunc():
    images = [] # List to store images
    className = [] # List to store student names
    usnNum = [] # List to store student USNs

    mylist = listPath() # Get list of image file paths from database

    if not mylist: # Check if 'mylist' list is empty
        print("Please register students.")
        return # Exit if no images are found

    # Loop through each image file in the directory
    for cl in mylist:
        curImg = cv2.imread(f'{cl}') # Read the image file
        images.append(curImg) # Add image to the list
        fnameExt = os.path.splitext(cl)[0] # Get file name without extension
        fnameS = re.split('/', fnameExt) # Split the path to get the name
        fname = re.split('_', fnameS[2]) # Split the name and USN
        className.append(fname[0]) # Add name to the list
        usnNum.append(fname[1]) # Add USN to the list

    # Function to find face encodings from images
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert the images from BGR format to RGB format (required by face_recognition)
            encoded_face = face_recognition.face_encodings(img)[0] # Encode the face in the image
            encodeList.append(encoded_face) # Add encoding to list
        return encodeList

    encoded_face_train = findEncodings(images) # Get the face encodings for the known student images

    # Function to mark attendance in the database
    def markAttendance(name,usn):
        name_a = check_A() # Get a list of students names who's attendance is already marked
        if name not in name_a: # If the name is not in the database, insert a new entry with the current time and date
            now = datetime.now() # Get current time
            time = now.strftime('%I:%M:%S %p') # Format time
            date = now.strftime('%d-%B-%Y') # Format date
            takeAttendance(date,time,name,usn) # Mark attendance

    cap = cv2.VideoCapture(0) # Open the webcam (camera)

    while True:
        success, img = cap.read() # Capture a frame from the webcam
        if not success: # If frame capture fails
            print('Failed to grab frame')
            break # Exit loop
        imgS = cv2.resize(img, (0,0), None, 0.25, 0.25) # Resize the captured frame to 1/4 of its original size for faster processing
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) # Covert the resized frame from bgr to rgb format
        faces_in_frame = face_recognition.face_locations(imgS) # Detect faces in the resized frame
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame) # Encode the detected faces

        for encoded_face, faceloc in zip(encoded_faces, faces_in_frame): # Loop through each detected face in the frame
            matches = face_recognition.compare_faces(encoded_face_train, encoded_face) # Compare the detected face with known faces
            faceDist = face_recognition.face_distance(encoded_face_train, encoded_face) # Calculate the face distance to find the best match
            matchIndex = np.argmin(faceDist)

            if matches[matchIndex]: # If a match is found, mark attendance and display the name
                name = className[matchIndex] # Get name of matched face
                usn = usnNum[matchIndex] # Get USN of matched face
                y1, x2, y2, x1 = faceloc # Get face location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 # Scale coordinates back to original size
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2) # Draw a rectangle around the detected face
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED) # Draw a filled rectangle for displaying the name
                cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) # Display the name on the frame
                try:
                    rq_response = rq.post('http://localhost:5000/tasks', json = {'task': name}) # Send POST request
                    rq_response.raise_for_status() # Raise an error for bad responses
                    # If successful, then mark attendance
                    markAttendance(name,usn) # Call the markAttendacne function to record attendance
                except rq.ConnectionError: # Handle connection error
                    print("Connection Error. Start the web server.")
                    cap.release() # Release webcam
                    cv2.destroyAllWindows() # Close OpenCV windows
                    return # Exit function

            else: # If no match is found
                y1, x2, y2, x1 = faceloc # Get face location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 # Scale coordinates back to original size
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2) # Draw a rectangle around the detected face
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED) # Draw a filled rectangle for displaying the name
                cv2.putText(img, "Not Registered", (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) # Display "Not Registered" on the frame
                try:
                    rq.post('http://localhost:5000/tasks', json = {'task': "Not Registered"}) # Send POST request
                except rq.ConnectionError: # Handle connection error
                    print("Connection Error. Start the web server.")
                    cap.release() # Release webcam
                    cv2.destroyAllWindows() # Release webcam
                    return # Exit function

        cv2.imshow('webcam', img) # Display the frame with detected faces and names

        k = cv2.waitKey(1) # Wait for key press
        if k%256 == 27: # Exit the loop when the 'Esc' key is pressed
            print("Escape hit, closing...")
            break # Exit loop

    cap.release() # Release the camera resource
    cv2.destroyAllWindows() # Close all OpenCV windows

if __name__ == '__main__':
    AttFunc() # Run the attendance function
