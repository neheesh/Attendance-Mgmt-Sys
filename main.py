#!/usr/bin/env python

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QVBoxLayout, QLabel, QTextEdit, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt
import threading

from regui import RegWindow
from attendance import AttFunc
from database import atlas_client
import webserver

class OutputRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.append(message)

    def flush(self):
        pass  # No need to implement flush method for this case

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.resize(600, 400)  # Increase initial width to accommodate both buttons and output
        self.center()  # Center the window

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a scroll area to contain the main layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow scroll area to resize widget inside
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        central_layout.addWidget(scroll_area)

        main_widget = QWidget()
        scroll_area.setWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        # Adding the welcome label
        welcome_label = QLabel("Attendance Management System")
        welcome_label.setAlignment(Qt.AlignCenter)  # Center align the text
        welcome_label.setStyleSheet("margin: 10px; padding: 20px; background-color: #282828; color: white; font-weight: bold; font-size: 26px; border-radius: 10px")  # Set background and text color
        main_layout.addWidget(welcome_label)

        # Creating the grid layout for the buttons
        button_layout = QGridLayout()

        button1 = QPushButton("Register Students")
        button2 = QPushButton("Take Attendacne")
        button3 = QPushButton("Reset Database")
        self.button4 = QPushButton("Start Web Server")

        button_style_t = """
            QPushButton {
                margin: 50px;
                margin-top: 100px;
                padding: 20px;
                font-size: 18px;
                border-radius: 10px;
                background-color: #d3d3d3;
                border: 1px solid #ababab;
            }
        """
        button_style_b = """
            QPushButton {
                margin: 50px;
                margin-bottom: 100px;
                padding: 20px;
                font-size: 18px;
                border-radius: 10px;
                background-color: #d3d3d3;
                border: 1px solid #ababab;
            }
        """
        clr_button_style = """
            QPushButton {
                margin: 10px;
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
                background-color: #d3d3d3;
                border: 1px solid #ababab;
            }
        """
        hover_style = """
            QPushButton:hover {
                background-color: #818589;
                color: #e5e4e2;
            }
        """

        button1.setStyleSheet(button_style_t + hover_style)
        button2.setStyleSheet(button_style_t + hover_style)
        button3.setStyleSheet(button_style_b + hover_style)
        self.button4.setStyleSheet(button_style_b + hover_style)

        button1.clicked.connect(self.open_window_reg)
        button2.clicked.connect(self.open_window_att)
        button3.clicked.connect(self.open_window_reset)
        self.button4.clicked.connect(self.toggle_flask_server)

        button_layout.addWidget(button1, 0, 0)
        button_layout.addWidget(button2, 0, 1)
        button_layout.addWidget(button3, 1, 0)
        button_layout.addWidget(self.button4, 1, 1)

        # Adding the grid layout to the main layout
        main_layout.addLayout(button_layout)

        # Creating the output window
        self.output_window = QTextEdit()
        self.output_window.setReadOnly(True)  # Make the output window read-only
        self.output_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy
        self.output_window.setStyleSheet("font-size: 16px; padding: 10px;")  # Set style sheet
        main_layout.addWidget(self.output_window)  # Add output window without stretch to avoid domination

        # Clear button for output window
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(clr_button_style + hover_style)
        clear_button.setFixedSize(90,60)
        clear_button.clicked.connect(self.clear_output)
        main_layout.addWidget(clear_button)

        #Redirect stdout to the QTextEdit
        sys.stdout = OutputRedirector(self.output_window)

        # List to keep references to the opened windows
        self.opened_windows = []
        self.server_thread = None  # Add a variable to keep track of the server thread

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

    def open_window_reg(self):
        self.output_window.append("Opening Registration Window")
        reg_window = RegWindow()
        reg_window.resetFields()
        reg_window.exec_()

    def open_window_att(self):
        self.output_window.append("Opening Camera For Attendance")
        AttFunc()

    def open_window_reset(self):
        self.output_window.append("Resetting Database")
        coll_names = ["students_a", "students_r"]
        folder = './student_images/'
        for coll_to_clr in coll_names:
            atlas_client.drop_all_documents(coll_to_clr)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                print(f"File removed {filename}")
                os.remove(file_path)
            except Exception as e:
                print(f"Could not remove the files. Error: {e}")

    def run_flask_server(self):
        self.output_window.append("Starting web server...")
        self.server_thread = webserver.run_server()

    def stop_flask_server(self):
        self.output_window.append("Stopping web server...")
        if self.server_thread:
            self.server_thread.shutdown()
            self.server_thread.join()
            self.server_thread = None

    def toggle_flask_server(self):
        if self.server_thread is None:
            self.run_flask_server()
            self.button4.setText("Stop Web Server")
        else:
            self.stop_flask_server()
            self.button4.setText("Start Web Server")

    def append_to_output(self, text):
        self.output_window.append(text)

    def clear_output(self):
        self.output_window.clear()

class Window(QWidget):
    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(150, 150, 300, 150)

        layout = QVBoxLayout()
        label = QLabel(f"This is {title}")
        layout.addWidget(label)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
