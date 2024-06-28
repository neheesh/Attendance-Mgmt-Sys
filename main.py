from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#import qtawesome as qta
import sys
import os

from regui import Window
from attendance import MainFunc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.setWindowTitle("Attendance Management System")
        self.setGeometry(100,100,300,400)

        self.label_1 = QLabel('Attendance Management System', self)
        self.label_1.resize(500,50)
        self.label_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_1.move(700,100)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Arial;
        font-size: 22px;
        """)

        self.initUI()

    def initUI(self):
        regButton = QPushButton("REGISTER", self)
        regButton.setToolTip('Register students to AMS')
        regButton.resize(400,50)
        regButton.move(750,470)
        regButton.setFont(QFont('Arial', 14))
        regButton.clicked.connect(self.openwindow)
        self.openwindow = Window()

        attButton = QPushButton("ATTENDANCE", self)
        attButton.setToolTip('Start recording attendance')
        attButton.resize(400,50)
        attButton.move(750,570)
        attButton.setFont(QFont('Arial', 14))
        attButton.clicked.connect(self.openwindow2)

    def openwindow(self):
        self.openwindow.exec()

    def openwindow2(self):
        MainFunc()
        os.system('sleep 2')
        os.system('libreoffice Attendance.csv')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
