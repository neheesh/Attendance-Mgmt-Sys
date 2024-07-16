import machine
import myrequest as requests
import network
from utime import sleep, sleep_ms
from machine import Pin, PWM

SSID = "minet"
PSK = "Ch3cH2o*"

ledZ = Pin("LED", Pin.OUT)
ledR = Pin(26, Pin.OUT)
ledB = Pin(21, Pin.OUT)
ledG = Pin(28, Pin.OUT)
ledZ.low()
ledR.low()
ledB.low()
ledG.low()

buzzer = PWM(Pin(19))
tones = {"B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62, "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494, "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951, "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978}

#song_R = ["E5","G5","A5","P","E5","G5","B5","A5","P","E5","G5","A5","P","G5","E5"]
#song_B = ["G5","B5","A5","P","E5","E5","G5","A5","P","E5","G5","A5","P","G5","E5"]
#song_G = ["G5","A5","P","G5","E5","E5","G5","A5","P","E5","G5","A5","P","G5","E5"]

#G_song = ["C4", "E4", "G4", "C5"]
#R_song = ["C5", "B4", "A4", "G4"]
#B_song = ["C5", "E5", "G5", "C6"]

error = [("C5", 200), ("E5", 200), ("G5", 200), ("C6", 200)]
reject = [("C5", 200), ("B4", 200), ("A4", 200), ("G4", 200)]
accept = [("C4", 500), ("E4", 500), ("G4", 500), ("C5", 500)]
idle = [("C5", 200), ("G5", 200), ("E5", 200), ("C5", 200)]

# def playtone(frequency):
#    buzzer.duty_u16(1000)
#    buzzer.freq(frequency)
#
# def bequiet():
#    buzzer.duty_u16(0)
#
# def playsong(mysong):
#    for i in range(len(mysong)):
#        if (mysong[i] == "P"):
#            bequiet()
#        else:
#            playtone(tones[mysong[i]])
#        sleep(0.3)
#    bequiet()

def play_song(sound):
    for note, duration in sound:
        frequency = tones.get(note)
        if frequency:
            pwm = machine.PWM(machine.Pin(19))  # Adjust Pin number based on your setup
            pwm.freq(frequency)
            pwm.duty_u16(1000)  # Adjust duty cycle as needed
            sleep_ms(duration)
            pwm.deinit()
        else:
            print(f"Unkown note: {note}")

def connect_to_wifi(ssid, psk):
    #Enable Wifi in Client Mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #Connect to Wifi, keep trying until failure or success
    wlan.connect(ssid, psk)
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to Connect")
        sleep(5)
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    print("Connected to WiFi")

def find(filter_dictionary,projection_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "attendancedb",
            "database": "attendance",
            "collection": "students_a",
            "filter": filter_dictionary,
            "projection": projection_dictionary,
        }
        response = requests.post(URL + "find", headers=headers, json=searchPayload)
        #print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            data = response.json()
            name_values = [document.get("name") for document in data.get("documents", [])]
            response.close()
            return name_values
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)

try:
    connect_to_wifi(SSID, PSK)

    url = "http://192.168.31.175:7788/tasks"
    URL = "https://ap-south-1.aws.data.mongodb-api.com/app/data-xbyudwb/endpoint/data/v1/action/"
    API_KEY = "eU4xMyLu4WwZEQKtWrcpeVJX6B98OVpFh9fYjdjG0o3qAZ9H1egheVUu6L8y1Y9T"

    while True:
        try:
            aName = requests.get(url)
            if aName is not None and aName.content:
                name = aName.json()['task']
                names = find({"name": name}, {"_id": 0, "name": 1})

                if name == "Not Registered":
                    ledR.value(1)
                    play_song(reject)
                    ledR.value(0)
                    sleep(1)
                elif name == "NONE":
                    ledZ.value(1)
                    play_song(idle)
                    ledZ.value(0)
                    sleep(1)
                elif names[0] == name:
                    ledG.value(1)
                    play_song(accept)
                    ledG.value(0)
                    sleep(1)
                else:
                    print("Name not found in the database.")
            else:
                print(f"Server responded with status code: {aName.status_code}")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")
            ledB.value(1)
            play_song(error)
            ledB.value(0)
            sleep(1)
        sleep(2.5)

except Exception as e:
    print(f"An error occurred: {e}")
