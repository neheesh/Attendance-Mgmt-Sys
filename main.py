#!/usr/bin/env python

# Importing necessary modules
import sys # System-specific parameters and functions
import os # Interact with the operating system
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QVBoxLayout, QLabel, QTextEdit, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt # Core functionalities like event handling and layouts
import threading # For running tasks in separate threads

# Importing custom modules and classes
from regui import RegWindow # Registration window UI
from attendance import AttFunc # Attendance function
from database import dropDocs # Drop all database documents
import webserver # Web server for Flask

# Class to redirect stdout to a QTextEdit widget
class OutputRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        self.text_edit.append(message) # Append messages to QTextEdit

    def flush(self):
        pass  # No need to implement flush method for this case

# Main window class for the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Attendance Management System") # Setting window title
        self.resize(600, 400)  # Set initial window size
        self.center()  # Center the window

        central_widget = QWidget() # Create central widget
        self.setCentralWidget(central_widget) # Set central widget

        # Create a scroll area to contain the main layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow scroll area to resize widget inside
        central_layout = QVBoxLayout() # Create central layout
        central_widget.setLayout(central_layout) # Set layout for central widget
        central_layout.addWidget(scroll_area) # Add scroll area to central layout

        main_widget = QWidget() # Create main widget for scroll area
        scroll_area.setWidget(main_widget) # Set main widget for scroll area

        main_layout = QVBoxLayout(main_widget) # Create main layout for main widget

        # Adding the welcome label
        welcome_label = QLabel("Attendance Management System")
        welcome_label.setAlignment(Qt.AlignCenter)  # Center align the text
        welcome_label.setStyleSheet("margin: 10px; padding: 20px; background-color: #282828; color: white; font-weight: bold; font-size: 26px; border-radius: 10px")  # Set background and text color
        main_layout.addWidget(welcome_label) # Add welcome label to main layout

        # Creating the grid layout for the buttons
        button_layout = QGridLayout()

        # Add welcome label to main layout
        button1 = QPushButton("Register Students")
        button2 = QPushButton("Take Attendacne")
        button3 = QPushButton("Reset Database")
        self.button4 = QPushButton("Start Web Server")

        # Define button styles
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
        clr_qt_button_style = """
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

        # Apply styles to buttons
        button1.setStyleSheet(button_style_t + hover_style)
        button2.setStyleSheet(button_style_t + hover_style)
        button3.setStyleSheet(button_style_b + hover_style)
        self.button4.setStyleSheet(button_style_b + hover_style)

        # Connect buttons to their functions
        button1.clicked.connect(self.open_window_reg)
        button2.clicked.connect(self.open_window_att)
        button3.clicked.connect(self.open_window_reset)
        self.button4.clicked.connect(self.toggle_flask_server)

        # Add buttons to the grid layout
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

        button_h_layout = QGridLayout() # Horizontal layout for clear and quit buttons

        # Clear button for output window
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(clr_qt_button_style + hover_style)
        clear_button.setFixedSize(90,60) # Set fixed size for the button
        clear_button.clicked.connect(self.clear_output) # Connect clear button to clear_output method
        button_h_layout.addWidget(clear_button, 0, 0)

        # Exit button to quit the application
        quit_button = QPushButton("Quit")
        quit_button.setStyleSheet(clr_qt_button_style + hover_style)
        quit_button.setFixedSize(90,60) # Set fixed size for the button
        quit_button.clicked.connect(self.quit_application) # Connect quit button to quit_application method
        button_h_layout.addWidget(quit_button, 0, 1)

        main_layout.addLayout(button_h_layout) # Add button layout to main layout

        #Redirect stdout to the QTextEdit
        sys.stdout = OutputRedirector(self.output_window)

        # List to keep references to the opened windows
        self.opened_windows = []
        self.server_thread = None  # Add a variable to keep track of the server thread

    # Center the window on the screen
    def center(self):
        screen = QApplication.primaryScreen().geometry() # Get screen geometry
        window = self.frameGeometry() # Get window geometry
        window.moveCenter(screen.center()) # Center window
        self.move(window.topLeft()) # Move window to top left of centered position

    # Open the registration window
    def open_window_reg(self):
        self.output_window.append("Opening Registration Window")
        reg_window = RegWindow()
        reg_window.resetFields() # Open the registration window
        reg_window.exec_() # Execute the registration window

    # Open the attendance window
    def open_window_att(self):
        self.output_window.append("Opening Camera For Attendance\nPress <Esc> to quit.")
        AttFunc() # Call the attendance function

    # Reset the database
    def open_window_reset(self):
        self.output_window.append("Resetting Database")
        folder = './student_images/' # Folder for student images
        dropDocs() # Drops the specified collections in database.py
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                print(f"File removed {filename}")
                os.remove(file_path) # Remove image files
            except Exception as e:
                print(f"Could not remove the files. Error: {e}")

    # Run the Flask server in a separate thread
    def run_flask_server(self):
        self.output_window.append("Starting web server...")
        try:
            self.output_window.append("Started web server.")
            self.server_thread = webserver.run_server() # Start the server
        except Exception as e:
            print(f'Error Occurred. {e}')

    # Stop the Flask server
    def stop_flask_server(self):
        self.output_window.append("Stopping web server...")
        try:
            if self.server_thread:
                self.server_thread.shutdown() # Shutdown the server
                self.server_thread.join() # Wait for the thread to finish
                self.server_thread = None
            self.output_window.append("Stopped web server.")
        except Exception as e:
            print(f'Error Occurred. {e}')

    # Toggle the Flask server on and off
    def toggle_flask_server(self):
        if self.server_thread is None:
            self.run_flask_server()
            self.button4.setText("Stop Web Server")
        else:
            self.stop_flask_server()
            self.button4.setText("Start Web Server")

    # Append text to the output window
    def append_to_output(self, text):
        self.output_window.append(text)

    # Clear the output window
    def clear_output(self):
        self.output_window.clear()

    # Quit the application
    def quit_application(self):
        if self.server_thread is not None:
            self.stop_flask_server()  # Call your method to stop the server if running
        QApplication.quit()

# Main method to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv) # Create a QApplication instance with command line arguments
    main_window = MainWindow() # Create an instance of the MainWindow class
    main_window.show() # Display the main window on the screen
    sys.exit(app.exec_()) # Display the main window on the screen
