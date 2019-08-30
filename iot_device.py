import requests
import json
import time
from datetime import datetime
import RPi.GPIO as GPIO
import sys
import os
import glob
import itertools, sys
from Spinner import Spinner

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
spinner = itertools.cycle(['-', '/', '|', '\\'])

my_device_id = "{your_Device_id}"

BASE_URL = 'https://snscoseiud.execute-api.us-west-2.amazonaws.com/IOT'

poll_url = 'https://snscoseiud.execute-api.us-west-2.amazonaws.com/IOT/device'
post_url = 'https://snscoseiud.execute-api.us-west-2.amazonaws.com/IOT/device'

temp_sensor = "/sys/bus/w1/devices/28-02131e0b69aa/w1_slave"


fetch_url = poll_url+'/commands/{}'.format(my_device_id)
status_url = post_url+'/status/{}'.format(my_device_id)

#pinouts
blinkerIO = 17
tempIO = 26

DEBUG = False

events = ['reboot', 'toggle_led', 'status', 'temp', 'geolocate', 'custom_command' ]

event_id = "0"


print("Running...... Device_id:{}".format(my_device_id))


class event(object):
    #event_id
    #timestamp
    #event_type
    #data
    #request_id

    pass


def get_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0

        return temp_f

def setupIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(blinkerIO,GPIO.OUT)
    GPIO.setup(tempIO,GPIO.OUT)
    

def blinker():
    GPIO.output(blinkerIO,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(blinkerIO,GPIO.LOW)
    

def handle_toggle_led(eventID,timestamp):
    #handle_toggle_led
    #print("TOGGLING LED...")
    if DEBUG:
        pass
    else:
        GPIO.output(tempIO,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(tempIO,GPIO.LOW)
        post_status(eventID,"OK",timestamp)
        

def handle_reboot(eventID,timestamp):
    #print("REBOOTING DEVICE...")
    post_status(eventID,"rebooting",timestamp)
    

def handle_read_temperature(eventID,timestamp):
    #print("READING TEMPERATURE...")
    post_status(eventID,get_temp(),timestamp)
        

def post_status(eventID, msg_data, timestamp):
    data = {'event_id' : eventID, 'timestamp': timestamp, 'eventType':'status', 'message': msg_data }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', "httpMethod": "POST"}
    requests.method = "POST"
    requests.httpBody = data

    try:
        response = requests.post(status_url, data=data_json, headers=headers)
        if DEBUG:
            print("data:   {}".format(data_json))
            print("Post Status response: {}".format(response))
        return response
    except:
        print("Unexpected error 1:", sys.exc_info()[0])
        

def handle_status(event_id, timestamp):
    if DEBUG:
        print("handle status...")
        
    #simulated systems data
    voltage = "5.00v"
    geolocation = "100 x 100"
    version = "v3.10"
    subsystems = "subsystems Ax100"
    network = "network strength: 55"

    temp = get_temp()

    msg_data = "voltage:{}, temp:{}, geo:{}, bus:{}, network:{},version:{}".format(voltage, temp, geolocation, subsystems, network, version)
    #msg_data = json.loads(msg_data)

    if DEBUG:
        print(msg_data)
    
    post_status(event_id, msg_data, timestamp)
    

def handle_commands(commands):
    if not commands:
        return
        #commands is all database columns

    for cmd in commands:
        #command id is random string in database
        try:
            event_id = cmd['id']
            timestamp = int(cmd['timestamp'])
        except:
            print("Unexpected error 6:", sys.exc_info()[0])

        print(event_id)

        command = cmd['data']

        if command =='toggle_led':
            handle_toggle_led(event_id,timestamp)

        elif command =='reboot':
            handle_reboot(event_id,timestamp)

        elif command =='read_temp':
            handle_read_temperature(event_id,timestamp)

        elif command =='status':
            handle_status(event_id, timestamp)


def fetch_commands():
    try:
        print"f:",sys.stdout.flush()
        url = BASE_URL+'/device/commands/{}'.format(my_device_id)
        response = requests.get(url)
        data = response.json()

        if data['Items']:
            print("#: {}").format(str(len(data['Items'])))
            return data['Items']

    except:
        print("Unexpected error 3:", sys.exc_info()[0])
        pass


setupIO()

while True:
    with Spinner():
        commands = fetch_commands()
        handle_commands(commands)
        #sys.stdout.write(".")
        #sys.stdout.flush()





