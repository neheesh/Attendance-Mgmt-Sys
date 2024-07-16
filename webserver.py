from flask import Flask, request, jsonify
import threading
import time
from werkzeug.serving import make_server

app = Flask(__name__)

# Data store (in-memory)
task = None
last_post_time = time.time()
reset_interval = 1  # Reset task after 1 seconds of inactivity

# Function to reset the task if no POST request
def reset_task():
    global task, last_post_time
    while True:
        time.sleep(1)  # Check every second
        if time.time() - last_post_time > reset_interval:
            task = "NONE"

# Start the background thread
reset_thread = threading.Thread(target=reset_task, daemon=True)
reset_thread.start()

# Route for handling GET requests
@app.route('/tasks', methods=['GET'])
def get_task():
    return jsonify({'task': task})

# Route for handling POST requests
@app.route('/tasks', methods=['POST'])
def add_task():
    global task, last_post_time
    task = request.json.get('task')
    last_post_time = time.time()
    return jsonify({'message': 'Task added successfully'}), 201

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def run_server():
    server_thread = ServerThread(app)
    server_thread.start()
    return server_thread

if __name__ == '__main__':
    run_server(debug=True)
