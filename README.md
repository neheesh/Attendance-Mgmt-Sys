# Attendance Management System Using Facial Recognition

This mini-project helps with attendance management using facial recognition by using Raspberry Pi Pico WH for indicating the user with LEDs and Buzzer. More about the microcontroller [README.md](./pyboard/README.md) and the code is in [/pyboard][./pyboard/*].

The code has a GUI programmed using `PyQt5`. Attach a screenshot.

1. Register Students
	- Runs `regui.py` which opens a window with input fields for `Student Name` and `USN` with two button `Ok` and `Cancel` on clicking opens up the webcam to save the `Student Name`, `USN` and `Image Path` in the database and image itself is saved locally on the machine in a directory called `student_images`.
2. Take Attendance
	- Runs `attendance.py` which requires at-least one student registered and the web-server running. If these conditions are satisfied, it opens up the webcam to detect the face, if the face is matched with registered face, marks the attendance and posts the name on detected face to the web-server.
3. Reset Database
	- Runs a function in `database.py` to drop all documents in the collections.
4. Start Web Server
	- Runs `webserver.py` as a background thread and starts the `WSIG` server with `Flask` app. If the web-server is running the button toggles to `Stop Web Server`.
5. Output Window
	- Shows all the print statements and instructions helping the user know what's going on.
6. Clear Button
	- Just clears the output window.
7. Quit Button
	- Quits the main window, if the web-server is running stops before exiting.

## Initialization and Setup

1. Set up a python virtual environment using `python -m venv [directory_name]`.
2. Install the requirements need for this project using `pip install -r requirements.txt`.
3. Make a directory called `student_images` if it does not exists on the local machine.
4. Get a account on `mongodb atlas`.
	- make a new `cluster`.
	- name the `database`.
	- create the `collections` for storing `attendance` and `registration`.
	- enable the Data API and get the `URL Endpoint` and `API Key`. (Used in micropython for initializing the mongodb for raspberry pi pico)
5. The `attendance.py` uses the `mongodb` driver connect. In `database.py` define the `ATLAS_URI`, `DB_NAME`, `COLL_NAME_A`, and `COLL_NAME_R` accordingly.
6. Specific port number can be assigned in `webserver.py` if needed. (Web server starts on 0.0.0.0 and port 5000 by default). If changed, the POST requests in `attendance.py` and GET requests in the micropython code that runs on 'raspberry pi pico wh' needs to changed accordingly.
7. Run `main.py` as `python main.py`.
