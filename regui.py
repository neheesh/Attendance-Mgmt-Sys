#!/usr/bin/env python

from PyQt5.QtWidgets import QDialog, QGroupBox, QLineEdit, QDialogButtonBox, QVBoxLayout, QFormLayout, QLabel, QApplication # Importing specific widgets from PyQt5.QtWidgets for creating the user interface
from PyQt5.QtGui import QFont # Importing QFont from PyQt5.QtGui for setting font styles
from PyQt5.QtCore import Qt # Importing Qt from PyQt5.QtCore for core functionalities like event handling
import sys # Importing system-specific parameters and functions
import os # Importing OS module to interact with the operating system
import cv2 # Importing OpenCV for image processing

# Importing the registerStudents function from database module
from database import registerStudents

# Creating a class that inherits the QDialog class
class RegWindow(QDialog):

    # Constructor
    def __init__(self):
        super(RegWindow, self).__init__() # Calling the constructor of the parent class

        self.setWindowTitle("Attendance Management System") # Setting window title
        self.setGeometry(100, 100, 300, 400) # Setting geometry to the window
        self.formGroupBox = QGroupBox("Registration") # Creating a group box for the form
        self.formGroupBox.setFont(QFont('Arial', 16)) # Setting font for the group box

        # creating input fields for name and USN
        self.usnLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()

        # Calling the method that create the form layout
        self.createForm()

        # Creating a dialog button for OK and Cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setFont(QFont('Arial', 16)) # Setting font for the button box

        # Connecting OK button to getInfo method
        self.buttonBox.accepted.connect(self.getInfo)

        # Connecting Cancel button to reject method
        self.buttonBox.rejected.connect(self.reject)

        # Creating a vertical layout for the dialog
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox) # Adding form group box to the layout
        mainLayout.addWidget(self.buttonBox) # Adding button box to the layout

        # Setting the layout for the dialog
        self.setLayout(mainLayout)

    # Method called when form is accepted
    def getInfo(self):

        print("Press <Space> to save the picture or <Esc> to quit.")

        cam = cv2.VideoCapture(0) # Open the default camera

        while True:
            ret, frame = cam.read() # Capture frame-by-frame
            if not ret:
                print('Failed to grab frame')
                break
            cv2.imshow("Register Image", frame) # Display the captured frame

            k = cv2.waitKey(1)
            if k%256 == 27: # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32: # SPACE pressed
                img_dir = "./student_images/"
                img_name = img_dir + "{}_{}.png".format(self.nameLineEdit.text(), self.usnLineEdit.text())
                cv2.imwrite(img_name, frame) # Save the captured image
                print('{} written. Registering...'.format(img_name))
                os.system('sleep 1') # Sleep for 1 second
                break

        cam.release() # Release the camera
        cv2.destroyAllWindows() # Close all OpenCV windows

        registerStudents(self.nameLineEdit.text(), self.usnLineEdit.text(), img_name) # Register the student with the captured image

        self.close() # Close the dialog window

    # Method to create the form layout
    def createForm(self):
        layout = QFormLayout() # Creating a form layout
        layout.addRow(QLabel("Student Name"), self.nameLineEdit) # Adding row for student name
        layout.addRow(QLabel("USN"), self.usnLineEdit) # Adding row for USN
        self.formGroupBox.setLayout(layout) # Setting layout for the form group box

    def resetFields(self):
        self.nameLineEdit.clear() # Clear the name input field
        self.usnLineEdit.clear() # Clear the USN input field

# Main method
if __name__ == '__main__':
    app = QApplication(sys.argv) # Create a PyQt5 application
    window = RegWindow() # Create an instance of the window
    window.show() # Show the window
    sys.exit(app.exec()) # Show the window
