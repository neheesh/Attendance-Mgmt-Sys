from flask import Flask, request, jsonify # Import necessary modules from Flask
import threading # Import threading module for background task
import time # Import time module for time-related operations
from werkzeug.serving import make_server # Import make_server for creating a WSGI server

app = Flask(__name__) # Create a Flask application instance

# Data store (in-memory)
task = None # Initialize task variable to None
last_post_time = time.time() # Record the time of the last POST request
reset_interval = 1  # Define the reset interval in seconds

# Function to reset the task if no POST request
def reset_task():
    global task, last_post_time
    while True:
        time.sleep(1)  # Wait for 1 second
        if time.time() - last_post_time > reset_interval:
            task = "NONE" # Reset task if no POST request within reset interval

# Start the background thread
reset_thread = threading.Thread(target=reset_task, daemon=True)
reset_thread.start()

# Route for handling GET requests
@app.route('/tasks', methods=['GET'])
def get_task():
    return jsonify({'task': task}) # Return the current task as JSON response

# Route for handling POST requests
@app.route('/tasks', methods=['POST'])
def add_task():
    global task, last_post_time
    task = request.json.get('task') # Update task with data from POST request
    last_post_time = time.time() # Update last POST time
    return jsonify({'message': 'Task added successfully'}), 201 # Return success message with status code 201

# Class to manage the Flask server in a separate thread
class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 5000, app) # Create a WSGI server with Flask app
        self.ctx = app.app_context() # Create an application context for the server
        self.ctx.push() # Push the context to activate it

    def run(self):
        self.server.serve_forever() # Start serving requests indefinitely

    def shutdown(self):
        self.server.shutdown() # Shutdown the server

# Function to start the Flask server in a new thread
def run_server():
    server_thread = ServerThread(app) # Create an instance of ServerThread with the Flask app
    server_thread.start() # Start the server thread
    return server_thread # Return the server thread instance

if __name__ == '__main__':
    run_server(debug=True) # Run the Flask server in debug mode if script is executed directly
