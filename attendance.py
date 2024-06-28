#!/usr/bin/env python

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
import re

def MainFunc():

    path = './student_images' #specify the path to the directory containing student images
    images = []
    className = []
    usnNum = []

    mylist = os.listdir(path) #get a list of image files in the specified directory

    #loop through each image file in the directory
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}') #read the image file
        images.append(curImg)
        fnameExt = os.path.splitext(cl)[0] #extract the class name (student's name) from the file name without the extension
        fname = re.split('_', fnameExt)
        className.append(fname[0]) #append the Name
        usnNum.append(fname[1]) #append the USN

        #className.append(os.path.splitext(cl)[0]) #extract the class name (student's name) from the file name without the extension

    #define a function to find face encodings from a list of images
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert the images from BGR format to RGB format (required by face_recognition)
            encoded_face = face_recognition.face_encodings(img)[0] #encode the face in the image
            encodeList.append(encoded_face)
        return encodeList

    encoded_face_train = findEncodings(images) #get the face encodings for the known student images

    #define a function to mark attendance
    def markAttendance(name,usn):
        with open('Attendance.csv', 'r+') as f: #open the attendance csv file in the read and write mode
            myDataList = f.readlines()
            nameList = []

            for line in myDataList: #extract existing names from the csv file
                entry = line.split(',')
                nameList.append(entry[0])

            if name not in nameList: #if the name is not in the csv file, add a new entry with the current time and date
                now = datetime.now()
                time = now.strftime('%I:%M:%S %p')
                date = now.strftime('%d-%B-%Y')
                f.writelines(f'\n{name}, {usn}, {time}, {date}')

    cap = cv2.VideoCapture(0) #open the webcam (camera)

    while True:
        success, img = cap.read() #capture a frame from the webcam
        if not success:
            print('Failed to grab frame')
            break
        imgS = cv2.resize(img, (0,0), None, 0.25, 0.25) #resize the captured frame to 1/4 of its original size for faster processing
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) #covert the resized frame from bgr to rgb format
        faces_in_frame = face_recognition.face_locations(imgS) #detect faces in the resized frame
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame) #encode the detected faces

        for encoded_face, faceloc in zip(encoded_faces, faces_in_frame): #loop through each detected face in the frame
            matches = face_recognition.compare_faces(encoded_face_train, encoded_face) #compare the detected face with known faces
            faceDist = face_recognition.face_distance(encoded_face_train, encoded_face) #calculate the face distance to find the best match
            matchIndex = np.argmin(faceDist)

            if matches[matchIndex]: #if a match is found, mark attendance and display the name
                name = className[matchIndex].upper().lower()
                usn = usnNum[matchIndex].upper().lower()
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 #scale coordinates back to original size
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2) #draw a rectangle around the detected face
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED) #draw a filled rectangle for displaying the name
                cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) #display the name on the frame
                markAttendance(name,usn) #call the markAttendacne function to record attendance
                cv2.rectangle(img, (x1, y2 + 10), (x2, y2), (0, 255, 0), cv2.FILLED) #show a green bar letting the user know

        cv2.imshow('webcam', img) #display the frame with detected faces and names

        k = cv2.waitKey(1)
        if k%256 == 27: #exit the loop when the 'Esc' key is pressed
            print("Escape hit, closing...")
            break

#        cap.release()
#        cv2.destroyAllWindows()

if __name__ == '__main__':
    MainFunc()
