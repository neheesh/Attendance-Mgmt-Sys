import machine # Importing the machine module for hardware control
import myrequest as requests # Importing a custom HTTP request module named `requests`
import network # Importing the network module for managing WiFi connections
from utime import sleep, sleep_ms # Importing sleep functions from utime module
from machine import Pin, PWM # Importing Pin and PWM classes from machine module

SSID = "<ssid>" # WiFi SSID
PSK = "<password>" # WiFi password

ledZ = Pin("LED", Pin.OUT) # Define Pin for on-board LED
ledR = Pin(26, Pin.OUT) # Define Pin for Red LED
ledB = Pin(21, Pin.OUT) # Define Pin for Blue LED
ledG = Pin(28, Pin.OUT) # Define Pin for Green LED
ledZ.low() # Turn off on-board LED
ledR.low() # Turn off Red LED
ledB.low() # Turn off Blue LED
ledG.low() # Turn off Green LED

buzzer = PWM(Pin(19)) # Define Pin for Buzzer and create PWM instance
# Dictionary mapping musical notes to frequencies
tones = {"B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62, "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494, "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951, "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978}

# Predefined musical sequences
error = [("C5", 200), ("E5", 200), ("G5", 200), ("C6", 200)]
reject = [("C5", 200), ("B4", 200), ("A4", 200), ("G4", 200)]
accept = [("C4", 500), ("E4", 500), ("G4", 500), ("C5", 500)]
idle = [("C5", 200), ("G5", 200), ("E5", 200), ("C5", 200)]

# Function to play a sequence of musical notes
def play_song(sound):
    for note, duration in sound:
        frequency = tones.get(note)
        if frequency:
            pwm = machine.PWM(machine.Pin(19))  # Create PWM instance for buzzer
            pwm.freq(frequency) # Set frequency of the PWM signal
            pwm.duty_u16(1000) # Set duty cycle of the PWM signal
            sleep_ms(duration) # Sleep for specified duration
            pwm.deinit() # Deinitialize PWM after playing note
        else:
            print(f"Unkown note: {note}")

# Function to connect to WiFi
def connect_to_wifi(ssid, psk):
    wlan = network.WLAN(network.STA_IF) # Initialize WiFi interface in station mode
    wlan.active(True) # Activate WiFi interface
    #Connect to Wifi, keep trying until failure or success
    #wlan.connect(ssid, psk) # Attempt to connect to WiFi
    max_attempts = 20
    attempt = 0
    while not wlan.isconnected() and wlan.status() >= 0: # Keep trying to connect until successful or failed
        wlan.connect(ssid, psk) # Attempt to connect to WiFi
        print("Waiting to Connect")
        ledZ.value(1)
        sleep(15) # Wait for 10 seconds before retrying
        ledZ.value(0)
        attempt += 1
    if not wlan.isconnected(): # If not connected after retries
        raise Exception("Wifi not available") # Raise exception indicating WiFi connection failure
        ledB.value(1)
        sleep(0.5)
        lebB.value(0)
    print("Connected to WiFi") # Raise exception indicating WiFi connection failure
    ledG.value(1)
    sleep(0.5)
    ledG.value(0)

# Function to query a database using a custom API
def find(filter_dictionary,projection_dictionary):
    try:
        headers = { "api-key": API_KEY } # Define headers for API request with API key
        searchPayload = { # Define payload for API request
            "dataSource": "<cluster name>",
            "database": "<database name>",
            "collection": "<collection name>",
            "filter": filter_dictionary,
            "projection": projection_dictionary,
        }
        response = requests.post(URL + "find", headers=headers, json=searchPayload) # Send POST request to API endpoint
        #print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300: # If request is successful
            data = response.json() # Parse JSON response
            name_values = [document.get("name") for document in data.get("documents", [])] # Extract names from documents
            response.close() # Close the response object
            return name_values # Return extracted names
        else: # If request is unsuccessful
            print(response.status_code) # Print HTTP status code
            print("Error")
        response.close() # Close the response object
    except Exception as e: # Catch any exceptions that occur during API request
        print(e)

try:
    connect_to_wifi(SSID, PSK) # Attempt to connect to WiFi using defined SSID and password

    url = "http://[IPADDR]:[PORT]/tasks" # Define URL for HTTP request
    URL = "<data endpoint>" # Define MongoDB API URL
    API_KEY = "<api-key>" # Define API key for authentication

    while True: # Main loop
        try:
            aName = requests.get(url) # Send GET request to retrieve task name from server
            if aName is not None and aName.content: # If response is valid and contains content
                name = aName.json()['task'] # Extract task name from JSON response
                names = find({"name": name}, {"_id": 0, "name": 1}) # Query database for matching names
                if name == "Not Registered": # If task name indicates not registered
                    ledR.value(1) # Turn on Red LED
                    play_song(reject) # Play rejection sound sequence
                    ledR.value(0) # Turn off Red LED after playing
                    #sleep(1) # Pause for 1 second
                elif name == "NONE": # If task name indicates no task
                    ledZ.value(1) # Turn on LED for idle state
                    play_song(idle) # Play idle sound sequence
                    ledZ.value(0) # Turn off LED after playing
                    #sleep(1) # Pause for 1 second
                elif names[0] == name: # If task name matches found name in database
                    ledG.value(1) # Turn on Green LED
                    play_song(accept) # Play acceptance sound sequence
                    ledG.value(0) # Turn off Green LED after playing
                    #sleep(1) # Pause for 1 second
                else: # If task name does not match any name in database
                    print("Name not found in the database.")
            else: # If server response is invalid or empty
                print(f"Server responded with status code: {aName.status_code}")
        except Exception as e: # Catch any exceptions that occur during server communication
            print(f"Failed to connect to the server: {e}")
            ledB.value(1) # Turn on Blue LED to indicate error
            play_song(error) # Play error sound sequence
            ledB.value(0) # Turn off Blue LED after playing
            #sleep(1) # Pause for 1 second
        sleep(1) # Pause for 2 seconds before repeating loop

except Exception as e: # Catch any exceptions that occur during program execution
    print(f"An error occurred: {e}")
