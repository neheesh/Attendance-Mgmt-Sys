#!/usr/bin/env python

# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import cv2

from database import registerStudents

# creating a class
# that inherits the QDialog class
class RegWindow(QDialog):

    # constructor
    def __init__(self):
        super(RegWindow, self).__init__()

        # setting window title
        self.setWindowTitle("Attendance Management System")

        # setting geometry to the window
        self.setGeometry(100, 100, 300, 400)

        # creating a group box
        self.formGroupBox = QGroupBox("Registration")

        self.formGroupBox.setFont(QFont('Arial', 16))

        self.usnLineEdit = QLineEdit()

        # creating a line edit
        self.nameLineEdit = QLineEdit()

        # calling the method that create the form
        self.createForm()

        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setFont(QFont('Arial', 16))

        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)

        # adding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

        # creating a vertical layout
        mainLayout = QVBoxLayout()

        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)

        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)

        # setting lay out
        self.setLayout(mainLayout)

    # get info method called when form is accepted
    def getInfo(self):

        print("Press <Space> to save the picture.")

        cam = cv2.VideoCapture(0)

        while True:
            ret, frame = cam.read()
            if not ret:
                print('Failed to grab frame')
                break
            cv2.imshow("Register Image", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                img_dir = "./student_images/"
                img_name = img_dir + "{}_{}.png".format(self.nameLineEdit.text(), self.usnLineEdit.text())
                cv2.imwrite(img_name, frame)
                #print('{} written!'.format(img_name))
                os.system('sleep 1')
                break
        cam.release()
        cv2.destroyAllWindows()
        registerStudents(self.nameLineEdit.text(), self.usnLineEdit.text(), img_name)

        # closing the window
        self.close()

    # create form method
    def createForm(self):

        # creating a form layout
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Student Name"), self.nameLineEdit)

        # for age and adding spin box
        layout.addRow(QLabel("USN"), self.usnLineEdit)

        # setting layout
        self.formGroupBox.setLayout(layout)

    def resetFields(self):
        self.nameLineEdit.clear()
        self.usnLineEdit.clear()

# main method
if __name__ == '__main__':

    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = RegWindow()

    # showing the window
    window.show()

    # start the app
    sys.exit(app.exec())
