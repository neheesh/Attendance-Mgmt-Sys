#!/usr/bin/env python

# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import cv2

# creating a class
# that inherits the QDialog class
class Window(QDialog):

    # constructor
    def __init__(self):
        super(Window, self).__init__()

        # setting window title
        self.setWindowTitle("Attendance Management System")

        # setting geometry to the window
        self.setGeometry(100, 100, 300, 400)

        # creating a group box
        self.formGroupBox = QGroupBox("Registration")

        self.formGroupBox.setFont(QFont('Arial', 16))

        # creating spin box to select age
        #self.ageSpinBar = QSpinBox()
        self.usnLineEdit = QLineEdit()

        # creating combo box to select degree
        #self.degreeComboBox = QComboBox()

        # adding items to the combo box
        #self.degreeComboBox.addItems(["BTech", "MTech", "PhD"])

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

        cam = cv2.VideoCapture(0)
        #cv2.namedWindow("Registering Image")
        #cam.set(cv2.CAP_PROP_FPS, 30.0)
        #cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        #cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
        #cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

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
                print('{} written!'.format(img_name))
                os.system('sleep 1')
                break
        cam.release()
        cv2.destroyAllWindows()

        # closing the window
        self.close()

    # create form method
    def createForm(self):

        # creating a form layout
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Student Name"), self.nameLineEdit)

        # for degree and adding combo box
        #layout.addRow(QLabel("Degree"), self.degreeComboBox)

        # for age and adding spin box
        layout.addRow(QLabel("USN"), self.usnLineEdit)

        # setting layout
        self.formGroupBox.setLayout(layout)

# main method
if __name__ == '__main__':

    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # showing the window
    window.show()

    # start the app
    sys.exit(app.exec())
